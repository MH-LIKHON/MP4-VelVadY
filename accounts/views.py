from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import ProfileUpdateForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView





# =======================================================
# ACCOUNTS VIEWS
# =======================================================

# ------------------------------- File Overview -------------------------------
# This file defines the views for login, registration, and logout user actions.





# =======================================================
# LOGIN VIEW
# =======================================================

# ------------------------------- Handles user login -------------------------------
def login_view(request):
    # Redirect logged-in users away from the login page
    if request.user.is_authenticated:
        return redirect("dashboard")

    # Check for new account flag to display success message
    if request.session.pop('new_account', None):
        messages.success(request, "Your account has been created. You can now log in.")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Attempts to authenticate the user with the provided email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'accounts/login.html')





# =======================================================
# REGISTER VIEW
# =======================================================

# ------------------------------- Handles new user registration -------------------------------
def register_view(request):
    # Prevent logged-in users from accessing the registration page
    if request.user.is_authenticated:
        return redirect("dashboard")  # Change to 'dashboard' if needed

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





# =======================================================
# LOGOUT VIEW
# =======================================================

# ------------------------------- Logs the user out and clears session -------------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")  # Adjust 'home' if using a different landing page





# =======================================================
# DASHBOARD VIEW
# =======================================================

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    # ------------------------------- Add user-specific dashboard context -------------------------------

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Placeholder data for future model integration
        context['active_subscriptions'] = 2
        context['last_order_date'] = '28 May 2025'
        context['remaining_credits'] = 18

        return context





# =======================================================
# PROFILE VIEW
# =======================================================

# ------------------------------- Shows current user's profile information -------------------------------
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")

# ------------------------------- Handles profile update form submission and display -------------------------------
@login_required
def profile_update_view(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'accounts/profile_update.html', {'form': form})





# =======================================================
# PASSWORD CHANGE VIEW
# =======================================================

# ------------------------------- Allows user to change password -------------------------------
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'  # Custom template for password change form
    success_url = reverse_lazy('password_change_done')  # Where to redirect after successful change

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)
