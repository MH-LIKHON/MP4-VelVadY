from django.shortcuts import render

# =======================================================
# CORE VIEWS
# =======================================================

# Render the homepage using the base layout and the home.html template
def home(request):
    return render(request, 'core/home.html')

# After successfull payment to thank you page route
def thank_you_view(request):
    return render(request, "core/thank_you.html")

# After unsuccessfull payment to cancel payment page route
def payment_cancelled_view(request):
    return render(request, 'core/payment_cancelled.html')