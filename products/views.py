from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Service
from .models import Service, Review
from .forms import ReviewForm





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
    })