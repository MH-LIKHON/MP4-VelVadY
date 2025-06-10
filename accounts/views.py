import os
from .models import CustomUser
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from products.models import Purchase
from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileUpdateForm, CustomUserRegistrationForm





# =======================================================
# LOGIN VIEW
# =======================================================

# Handles login views for users
def login_view(request):
    """
    Handles the login functionality for users. Authenticates user credentials,
    sets session messages, and redirects based on login status.
    """

    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    # Display message if the user came from a Stripe route
    if 'next' in request.GET and 'checkout-session' in request.GET['next']:
        messages.info(request, "Please log in or create an account to continue with your purchase.")

    # Show registration success message
    if request.session.pop('new_account', None):
        messages.success(request, "Your account has been created. You can now log in.")

    # Handle login form
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")

            next_url = request.GET.get('next')

            # Handle Stripe special case: avoid redirecting to a POST-only route
            if next_url and next_url.startswith("/products/create-checkout-session/"):
                try:
                    # Extract service ID from the path
                    service_id = next_url.strip("/").split("/")[-1]
                    # Import Service model and get the slug
                    from products.models import Service
                    service = Service.objects.get(id=service_id)
                    # Redirect to safe slug-based view
                    return redirect("service_detail", slug=service.slug)
                except Exception:
                    # Fallback if service is not found
                    return redirect("product_list")

            # Safe redirect to intended destination
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            # Final fallback
            return redirect("dashboard")

        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'accounts/login.html')






# =======================================================
# REGISTER VIEW
# =======================================================

# Handles new user registration
def register_view(request):
    """
    Processes the registration form, validates user input,
    and creates a new user account if all fields are valid.
    """

    # Prevent logged-in users from accessing the registration page
    if request.user.is_authenticated:
        return redirect("dashboard")

    # Remove any existing new account flag from session
    request.session.pop('new_account', None)

    if request.method == "POST":
        # Populate the form with submitted POST data
        form = CustomUserRegistrationForm(request.POST)

        # Validate form input
        if form.is_valid():
            # Save the user to the database
            user = form.save()

            # Prepare the full dashboard URL
            protocol = 'https' if not settings.DEBUG else 'http'
            domain = os.getenv('DOMAIN', get_current_site(request).domain)
            dashboard_path = reverse('dashboard')
            full_dashboard_url = f"{protocol}://{domain}{dashboard_path}"

            # Prepare email details
            subject = 'Welcome to VelVady'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            context = {
                'user': user,
                'service': service,
                'amount_paid': purchase.amount_paid,
                'purchase': purchase,
                'dashboard_url': f"{protocol}://{domain}{reverse('dashboard')}",
                'protocol': protocol,
                'domain': domain,
            }
            html_content = render_to_string('accounts/welcome_email.html', context)

            # Create the email
            email = EmailMultiAlternatives(subject, '', from_email, [to_email])
            email.attach_alternative(html_content, "text/html")
            email.send()

            # Flag session to show login success message
            request.session['new_account'] = True

            # Redirect the user to the login page after registration
            return redirect("login")

        else:
            # Show error message if form is invalid
            messages.error(request, "Please correct the errors below.")
    else:
        # Initialise an empty registration form on GET request
        form = CustomUserRegistrationForm()

    # Display Registration Page
    return render(request, 'accounts/register.html', {"form": form})





# =======================================================
# LOGOUT VIEW
# =======================================================

# Logs the user out and clears session
def logout_view(request):
    """
    Logs out the currently authenticated user, clears the session,
    and redirects them to the home page with a success message.
    """

    # Terminate the user's session and log them out
    logout(request)

    # Display a logout confirmation message
    messages.success(request, "You have been logged out successfully.")

    # Redirect to the home page
    return redirect("home")





# =======================================================
# DASHBOARD VIEW
# =======================================================

# Handles user dashboard and displays purchase history
class DashboardView(LoginRequiredMixin, TemplateView):
    # Specifies the HTML template to render for the dashboard
    template_name = 'accounts/dashboard.html'

    # Adds user-specific context data including purchase records and metrics
    def get_context_data(self, **kwargs):
        """
        Prepares the dashboard view context with user's purchase history
        and key metrics like total services, total amount spent, and last order date.
        """
        from django.db.models import Sum

        # Get the base context from the parent TemplateView
        context = super().get_context_data(**kwargs)

        # Get all purchases by the current user
        user = self.request.user
        purchases = Purchase.objects.filter(user=user).select_related('service')

        # Calculate total services purchased
        total_services = purchases.count()

        # Calculate total amount spent (use 0 if none)
        total_spent = purchases.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        # Get the timestamp of the latest purchase
        latest_purchase = purchases.order_by('-timestamp').first()
        last_order_date = latest_purchase.timestamp if latest_purchase else None

        # Pass values into the template context
        context['purchases'] = purchases
        context['total_services'] = total_services
        context['total_spent'] = total_spent
        context['last_order_date'] = last_order_date

        return context





# =======================================================
# PROFILE VIEW
# =======================================================

# Shows current user's profile information
@login_required
def profile_view(request):
    """
    Displays the logged-in user's profile page.
    The view is protected to ensure only authenticated users can access it.
    """
    return render(request, "accounts/profile.html")

# Handles profile update form submission and display
@login_required
def profile_update_view(request):
    """
    Handles both the display and processing of the profile update form.
    Loads the user's current information and updates it if valid data is submitted.
    """
    # Retrieves the currently logged-in user's object
    user = get_object_or_404(CustomUser, pk=request.user.pk)

    if request.method == 'POST':
        # Binds form data to the user instance for validation and saving
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Pre-fills the form with the user's existing information for editing
        form = ProfileUpdateForm(instance=user)

    # Renders the profile update form page with the current form state
    return render(request, 'accounts/profile_update.html', {'form': form})





# =======================================================
# PASSWORD CHANGE VIEW
# =======================================================

# Handles password update for logged-in users
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# Password change views
class CustomPasswordChangeView(PasswordChangeView):
    """
    Displays the password change form to authenticated users and handles validation.
    Uses a custom template and redirects to a confirmation page upon success.
    """

    template_name = 'accounts/password_change.html'

    # Redirects user after successful password change
    success_url = reverse_lazy('password_change_done')

    form_class = PasswordChangeForm

    def form_valid(self, form):
        """
        Adds a success message once the password has been changed successfully.
        """
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)





# =======================================================
# PASSWORD RESET VIEW
# =======================================================

# Sends email using both plain text and HTML templates
class CustomPasswordResetView(PasswordResetView):
    """
    Overrides send_mail() to send both HTML and plain versions of password reset email.
    """
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context).strip()
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()