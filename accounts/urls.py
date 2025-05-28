from django.urls import path
from . import views

# =======================================================
# ACCOUNTS APP ROUTES
# =======================================================

# This file defines the routes for login, register, and other user actions

urlpatterns = [
    # Route to the login page
    path('login/', views.login_view, name='login'),

    # Route to the registration page
    path('register/', views.register_view, name='register'),
]