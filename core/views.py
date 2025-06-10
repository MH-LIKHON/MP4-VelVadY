from .forms import ContactForm
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from products.models import Purchase
from django.core.mail import send_mail
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

            # Extract user input from the validated form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Compose the subject line and full message body
            subject = f"New Contact Message from {name}"
            full_message = f"You have received a new message from {name} ({email}):\n\n{message}"

            # Send the email to the admin address configured in settings.py
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

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
