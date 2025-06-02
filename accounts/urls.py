from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView





# =======================================================
# ACCOUNTS APP ROUTES
# =======================================================

# ------------------------------- This file defines the routes for login, register, and logout -------------------------------

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

    # Password change route
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    # Password change services
    path('services/', TemplateView.as_view(template_name='core/services.html'), name='services'),
]