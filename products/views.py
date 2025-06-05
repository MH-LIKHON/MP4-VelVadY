import os
import stripe
from .models import Service
from .forms import ReviewForm
from django.urls import reverse
from django.conf import settings
from .models import Service, Review
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
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

# Used to exempt this view from CSRF protection for POST testing
from django.views.decorators.csrf import csrf_exempt

# Used to fetch secret key and build full URLs
from django.conf import settings

# Used to return JSON or error responses
from django.http import JsonResponse, HttpResponseBadRequest

# Stripe API client
import stripe

# Import the Service model to fetch the relevant service for checkout
from .models import Service

# Set the Stripe secret key using the settings file
stripe.api_key = settings.STRIPE_SECRET_KEY

# This view creates a Stripe Checkout Session for a selected service
@csrf_exempt
def create_checkout_session(request, service_id):
    """
    Handles a POST request to initialise a Stripe Checkout Session for a specific service.
    Redirects the user to Stripe’s secure hosted checkout page.
    """

    # Only allow POST requests to create a checkout session
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        # Attempt to retrieve the service using the provided ID
        service = Service.objects.get(id=service_id)

        # Use your actual deployment domain here (GitHub Codespaces domain or localhost)
        domain_url = DOMAIN

        # Create the Stripe Checkout Session with price and product details
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],     # Accept card payments
            mode="payment",                    # One-time payment mode
            line_items=[{
                "price_data": {
                    "currency": "gbp",         # Currency for the payment
                    "unit_amount": int(service.price * 100),  # Convert pounds to pence
                    "product_data": {
                        "name": service.title,
                        "description": service.description,
                    },
                },
                "quantity": 1,
            }],

            # Redirect after successful payment
            success_url = f"{DOMAIN}/thank-you/",

            # Redirect if payment is cancelled
            cancel_url = f"{DOMAIN}/cancelled/",
        )

        # Optional: log session info for debugging
        print("Stripe session created:", session.url)

        # Return the session ID to the frontend so Stripe.js can redirect
        return JsonResponse({'id': session.id})

    except Service.DoesNotExist:
        # If service ID is invalid or not found
        return HttpResponseBadRequest("Service not found")

    except Exception as e:
        # Log any other error for debugging
        print("Stripe error:", e)
        return JsonResponse({'error': 'Could not start checkout. Try again.'}, status=500)