from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomUserRegistrationForm


# =======================================================
# ACCOUNTS VIEWS
# =======================================================

# Renders the login page and handles authentication for users attempting to log in
def login_view(request):
    if request.session.pop('new_account', None):
        messages.success(request, "Your account has been created. You can now log in.")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Attempts to authenticate the user with the provided email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Logs the user in and creates a session
            messages.success(request, "Welcome back!")
            return redirect("home")  # Adjust this to the correct landing page
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'accounts/login.html')


# Handles registration form submission, user creation, and error reporting
def register_view(request):
    # Prevent logged-in users from accessing the registration page
    if request.user.is_authenticated:
        return redirect("home")  # Change to 'dashboard' if needed

    # Clean up session flag if it exists
    request.session.pop('new_account', None)

    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new user to the database
            request.session['new_account'] = True  # Triggers message on login page
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserRegistrationForm()  # Instantiates an empty form for GET requests

    return render(request, 'accounts/register.html', {"form": form})