from . import views
from django.urls import path
from .views import CustomPasswordResetView
from products.views import product_list_view
from django.views.generic import TemplateView
from .views import CustomPasswordChangeDoneView
from django.contrib.auth import views as auth_views





# =======================================================
# ACCOUNTS APP ROUTES
# =======================================================

urlpatterns = [

    # Route to the login page
    path('login/', views.login_view, name='login'),

    # Route to the registration page
    path('register/', views.register_view, name='register'),

    # Route to log the user out and redirect them
    path('logout/', views.logout_view, name='logout'),

    # Route to dashboard page for logged-in users
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Route to profile page for logged-in users
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_update_view, name='profile_edit'),

    # Route to service list
    path('services/', product_list_view, name='services'),

    # Route to password reset done page
    path('password/change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    # Password change views
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),

    # Form to enter email
    path('password-reset/', CustomPasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.txt',
        html_email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
    ), name='password_reset'),

    # Email sent confirmation page
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    # Link from email opens reset form
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

    # Final confirmation after password is reset
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]