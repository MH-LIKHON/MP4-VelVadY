import os
import stripe
from .models import Service
from .forms import ReviewForm
from django.urls import reverse
from django.conf import settings
from .models import Service, Review
from .models import Service, Purchase
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

DOMAIN = os.getenv("DOMAIN", "http://127.0.0.1:8000")




# =======================================================
# PRODUCT LIST VIEW
# =======================================================

# Views for product lists
def product_list_view(request):
    # This queries all services marked as active from the database
    services = Service.objects.filter(is_active=True)

    # This renders the product list template with the list of services as context
    return render(request, 'products/product_list.html', {'services': services})





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

# Creates a Stripe Checkout Session for logged-in users only

@csrf_exempt
def create_checkout_session(request, service_id):
    """
    Ensures that only authenticated users can initiate the Stripe Checkout process.
    If the user is not logged in, they are redirected to the login page with a return path.
    """

    # Redirect unauthenticated users to login page
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    # Only allow POST requests to create a checkout session
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        # Attempt to retrieve the service
        stripe.api_key = settings.STRIPE_SECRET_KEY
        service = Service.objects.get(id=service_id)

        # Use your actual deployment domain here
        domain_url = DOMAIN

        # Create the Stripe Checkout Session with product details
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
            success_url=f"{domain_url}/thank-you/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_url}/cancelled/",
        )

        # Optional: log session info
        print("Stripe session created:", session.url)

        # Return session ID to frontend
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
        # Retrieve the Stripe session
        session = stripe.checkout.Session.retrieve(session_id)

        # Get line items to extract service details
        line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
        line_item = line_items.data[0]

        # Get metadata added during checkout (e.g. service_id)
        service_id = session.metadata.get('service_id')
        amount_paid = session.amount_total / 100  # Stripe uses cents

        # Prevent duplicate purchases
        if not Purchase.objects.filter(stripe_session_id=session_id).exists():
            Purchase.objects.create(
                user=request.user,
                service_id=service_id,
                amount_paid=amount_paid,
                stripe_session_id=session_id
            )

        return render(request, 'products/checkout_success.html', {
            'session': session
        })

    except Exception as e:
        print(f"Stripe error: {e}")
        return redirect('home')