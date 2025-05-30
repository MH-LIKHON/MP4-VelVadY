from django.urls import path
from . import views

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
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Route to profile page for logged-in users
    path('profile/', views.profile_view, name='profile'),
]
