from .forms import ContactForm
from django.shortcuts import render
from django.contrib import messages
from products.models import Purchase
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required





# =======================================================
# CORE VIEWS
# =======================================================

# Core views
def home(request):
    """
    Renders the homepage using the base layout.
    """
    return render(request, 'core/home.html')





# =======================================================
# CONTACT VIEWS
# =======================================================

# Contact views
def contact_view(request):
    """
    Handles both displaying and processing of the contact form.
    Renders the form on GET request and processes the submission on POST.
    """
    
    # Handle POST Request
    if request.method == 'POST':
        form = ContactForm(request.POST)

        # If the submitted form is valid, show success and reset
        if form.is_valid():
            form.save()
            # Normally, we would send an email here or store the message
            messages.success(request, "We’ve received your message. A member of our team will be in touch shortly.")
            return redirect('contact')
        else:
            # If the form is invalid, show errors
            messages.error(request, 'Please correct the errors below.')

    else:
        # Show a blank form when first visiting the page
        form = ContactForm()

    # Render the Template
    return render(request, 'core/contact.html', {'form': form})





# =======================================================
# THANK YOU VIEWS
# =======================================================

# Post purchase thank you views
@login_required
def thank_you_view(request):
    """
    Renders the thank you page after a successful payment.
    Displays the latest purchase made by the logged-in user.
    """
    last_purchase = Purchase.objects.filter(user=request.user).order_by('-timestamp').first()

    return render(request, 'core/thank_you.html', {
        'purchase': last_purchase
    })





# =======================================================
# CANCELLED VIEWS
# =======================================================

# Cancelled purchase views
def payment_cancelled_view(request):
    """
    Renders the payment cancelled page when a Stripe transaction is aborted.
    No charges are processed.
    """
    return render(request, 'core/payment_cancelled.html')





# =======================================================
# LEGAL: Terms and Privacy
# =======================================================

# Renders the Terms & Privacy page
def terms_and_policy(request):
    """
    Displays the combined Terms & Conditions and Privacy Policy.
    """
    return render(request, 'core/terms_and_policy.html')





# =======================================================
# TEMPORARY: 404 page preview route (for testing only)
# =======================================================

# Renders 404 page
def custom_404(request, exception=None):
    """
    Handles 404 errors with a custom template and proper status code.
    """
    return render(request, 'core/404.html', status=404)