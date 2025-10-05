from . import views
from django.urls import path





# =======================================================
# CORE APP ROUTES (namespaced)
# =======================================================

# Allows reverse('core:payment_cancelled') etc.
app_name = 'core'

# This file defines the URL patterns for the core app.
urlpatterns = [
    # Route the base URL to the homepage view
    path('', views.home, name='home'),

    # Route to contact page
    path('contact/', views.contact_view, name='contact'),

    # Route to t&c page
    path('legal/', views.terms_and_policy, name='terms_and_policy'),

    # Alias for Stripe or external links using /terms
    path('terms/', views.terms_and_policy, name='terms'),

    # Route to payment cancelled
    path('cancelled/', views.payment_cancelled_view, name='payment_cancelled'),
]