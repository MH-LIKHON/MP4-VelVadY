from . import views
from django.urls import path





# =======================================================
# CORE APP ROUTES
# =======================================================

# This file defines the URL patterns for the core app.
urlpatterns = [
    # Route the base URL to the homepage view
    path('', views.home, name='home'),

    # Route to thank you page
    path("thank-you/", views.thank_you_view, name="thank_you"),

    # Route to cancelled payment page
    path('cancelled/', views.payment_cancelled_view, name='payment_cancelled'),

    # Route to contact page
    path('contact/', views.contact_view, name='contact'),
]
