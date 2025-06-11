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

        domain = os.getenv("DOMAIN", "https://velvady-app-b7f67234cb3b.herokuapp.com")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            customer_email=request.user.email,
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
    Sends a confirmation email only if the purchase is new.
    """

    # Retrieve session ID from query string
    session_id = request.GET.get('session_id')

    if not session_id:
        # If no session ID is provided, redirect to homepage
        return redirect('home')

    try:
        # Set the API key to use Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Retrieve the full Stripe checkout session
        session = stripe.checkout.Session.retrieve(session_id)

        # Retrieve line items to extract the service purchased
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        line_item = line_items.data[0]

        # Extract service ID and calculate paid amount
        service_id = session.metadata.get('service_id')
        amount_paid = session.amount_total / 100  # Convert from pence to pounds

        # Retrieve the service object
        service = Service.objects.get(id=service_id)

        # Create or retrieve the purchase record
        purchase, created = Purchase.objects.get_or_create(
            stripe_session_id=session_id,
            defaults={
                'user': request.user,
                'service': service,
                'amount_paid': amount_paid,
            }
        )

        # Only send confirmation email if the purchase was newly created
        if created:
            # Prepare email content
            subject = f"Order Confirmation - {service.title}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = request.user.email

            context = {
                'user': request.user,
                'purchase': purchase,
                'service': service,
                'amount_paid': amount_paid,
                'protocol': 'https' if not settings.DEBUG else 'http',
                'domain': os.getenv('DOMAIN', 'velvady-app-b7f67234cb3b.herokuapp.com'),
            }

            html_content = render_to_string('accounts/order_confirmation_email.html', context)

            email = EmailMultiAlternatives(subject, '', from_email, [to_email])
            email.attach_alternative(html_content, "text/html")
            email.send()

        # Render the thank you page with purchase summary
        return render(request, 'core/thank_you.html', {
            'user': request.user,
            'purchase': purchase,
            'service': service,
            'amount_paid': amount_paid,
        })

    except Exception as e:
        print(f"Error in checkout_success: {e}")
        return redirect('home')






# =======================================================
# STRIPE WEBHOOK HANDLER
# =======================================================

@csrf_exempt
def stripe_webhook(request):
    """
    Handles Stripe webhook events for completed checkout sessions.
    Verifies the Stripe signature, parses the event, and records
    a new purchase if the payment was successful.
    """

    # Get the raw request body from Stripe
    payload = request.body

    # Get the Stripe signature header
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    # Get the Stripe webhook secret from environment variables
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        # Validate and construct the event using Stripe's library
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

    except ValueError as e:
        # Return 400 if payload is invalid
        return HttpResponseBadRequest("Invalid payload")

    except stripe.error.SignatureVerificationError as e:
        # Return 400 if signature is invalid
        return HttpResponseBadRequest("Invalid signature")

    if event['type'] == 'checkout.session.completed':

        # Extract the session object from the webhook event
        session = event['data']['object']

        # Get the session ID
        session_id = session.get('id')

        # Retrieve metadata set during session creation (e.g. service ID)
        service_id = session['metadata'].get('service_id')

        # Get the email of the Stripe customer
        user_email = session.get('customer_email')

        # Convert the amount from pence to pounds
        amount_paid = session.get('amount_total', 0) / 100

        try:
            # Fetch the user based on their email address
            user = User.objects.get(email=user_email)

            # Fetch the service that was purchased
            service = Service.objects.get(id=service_id)

            # Create the purchase record if it does not already exist
            Purchase.objects.get_or_create(
                stripe_session_id=session_id,
                defaults={
                    'user': user,
                    'service': service,
                    'amount_paid': amount_paid,
                }
            )

        except Exception as e:
            # Log any error for debugging
            print(f"Webhook error: {e}")

    # Respond to Stripe with success to avoid repeated webhook calls
    return JsonResponse({'status': 'success'})
