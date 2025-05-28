from django.shortcuts import render

# =======================================================
# ACCOUNTS VIEWS
# =======================================================

# Render the login page template when users visit /accounts/login/
def login_view(request):
    return render(request, 'accounts/login.html')

# Render the registration page template when users visit /accounts/register/
def register_view(request):
    return render(request, 'accounts/register.html')