from django.urls import path
from . import views

# =======================================================
# CORE APP ROUTES
# =======================================================

# This file defines the URL patterns for the core app.
# I am currently routing the root URL to the home view.

urlpatterns = [
    # Route the base URL to the homepage view
    path('', views.home, name='home'),
]
