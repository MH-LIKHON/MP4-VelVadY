import os
import stripe
from .forms import ReviewForm
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from .models import Service, Review, Purchase
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

DOMAIN = os.getenv("DOMAIN", "http://127.0.0.1:8000")




# =======================================================
# PRODUCT LIST VIEW
# =======================================================

def product_list_view(request):
    """
    Displays a list of active services.
    Supports optional filtering by search query (title or description)
    and category.
    """

    # Get the search query and category from GET parameters
    query = request.GET.get('q')
    category = request.GET.get('category')

    # Start with all active services
    services = Service.objects.filter(is_active=True)

    # Filter by search query if provided
    if query:
        services = services.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Filter by category if provided
    if category:
        services = services.filter(category__iexact=category)

    # Prepare context for template
    context = {
        'services': services,
        'query': query,
        'category': category,
    }

    # Render the product list template with filtered services
    return render(request, 'products/product_list.html', context)





# =======================================================
# SERVICE DETAIL VIEW
# =======================================================

# Detail view for individual services with review support
def service_detail_view(request, slug):

    # This retrieves the service object based on the provided slug or returns 404 if not found
    service = get_object_or_404(Service, slug=slug)

    # This gets all reviews related to the service, sorted by most recent
    reviews = Review.objects.filter(service=service).order_by('-created_at')

    # If the request is a POST, it means the user is submitting a review
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Save the form without committing to add user and service manually
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.service = service
            new_review.save()

            # Redirect back to the same service page to avoid resubmission on refresh
            return redirect('service_detail', slug=slug)
    else:
        # If GET request, instantiate an empty review form
        review_form = ReviewForm()

    # This renders the service detail page with service info, reviews, and the review form
    return render(request, 'products/service_detail.html', {
        'service': service,
        'reviews': reviews,
        'review_form': review_form,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    })





# =======================================================
# STRIPE CHECKOUT SESSION
# =======================================================

@require_POST
@login_required
def create_checkout_session(request, service_id):
    """
    Creates a Stripe Checkout Session for logged-in users only.
    """

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        service = Service.objects.get(id=service_id)

        domain_url = DOMAIN

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "gbp",
                    "unit_amount": int(service.price * 100),
                    "product_data": {
                        "name": service.title,
                        "description": service.description,
                    },
                },
                "quantity": 1,
            }],
            metadata={
                "service_id": service.id
            },
            success_url = domain_url + "/products/thank-you/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=f"{domain_url}/cancelled/",
        )

        return JsonResponse({'id': session.id})

    except Service.DoesNotExist:
        return HttpResponseBadRequest("Service not found")

    except Exception as e:
        print("Stripe error:", e)
        return JsonResponse({'error': 'Could not start checkout. Try again.'}, status=500)
    




# =======================================================
# STRIPE CHECKOUT SUCCESS HANDLER
# =======================================================

# Handles post-payment success logic and saves purchase
@login_required
def checkout_success(request):
    """
    Handles a successful Stripe checkout by retrieving the session,
    verifying the payment, and recording the purchase in the database.
    """

    session_id = request.GET.get('session_id')

    if not session_id:
        # No session ID found in query string
        return redirect('home')

    try:
        # Set API key for Stripe API calls
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Retrieve the Stripe checkout session object by session_id
        session = stripe.checkout.Session.retrieve(session_id)

        # Retrieve line items for the session to get service details
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        line_item = line_items.data[0]

        # Extract service_id from metadata (set during checkout creation)
        service_id = session.metadata.get('service_id')
        amount_paid = session.amount_total / 100  # Convert pence to pounds

        # Check if purchase already exists to avoid duplicates
        if not Purchase.objects.filter(stripe_session_id=session_id).exists():
            # Get the Service object from database
            service = Service.objects.get(id=service_id)

            # Create Purchase record for this successful transaction
            purchase = Purchase.objects.create(
                user=request.user,
                service=service,
                amount_paid=amount_paid,
                stripe_session_id=session_id
            )

            # Prepare email subject and sender
            subject = f"Order Confirmation - {service.title}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = request.user.email  # Send to logged-in user email

            # Prepare context for rendering email template
            context = {
                'user': request.user,
                'purchase': purchase,
                'service': service,
                'amount_paid': amount_paid,
            }

            # Render HTML content from the email template
            html_content = render_to_string('accounts/order_confirmation_email.html', context)

            # Create the email message object
            email = EmailMultiAlternatives(subject, '', from_email, [to_email])

            # Attach the HTML content as alternative
            email.attach_alternative(html_content, "text/html")

            # Send the email
            email.send()

            # --- END: Send Order Confirmation Email ---

        # Redirect user to thank you page after success
        return redirect('thank_you')

    except Exception as e:
        # Log or print the exception (optional)
        print(f"Error in checkout_success: {e}")

        # Redirect to home page on failure
        return redirect('home')