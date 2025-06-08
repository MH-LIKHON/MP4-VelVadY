from django.shortcuts import render
from products.models import Purchase
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