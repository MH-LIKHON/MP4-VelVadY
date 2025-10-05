from . import views
from django.urls import path
from .views import stripe_webhook
from .views import product_list_view
from .views import create_checkout_session





# =======================================================
# URL PATTERNS FOR PRODUCTS APP
# =======================================================

# This file defines the routes
urlpatterns = [

    # This URL shows all active services in a grid layout
    path('services/', views.product_list_view, name='product_list'),

    # This URL displays a specific service based on its slug
    path('products/<slug:slug>/', views.service_detail_view, name='service_detail'),

    # This routes to exolore services page
    path('accounts/services/', product_list_view, name='service_list'),

    # This routes to stripe checkout services
    path('create-checkout-session/<int:service_id>/', create_checkout_session, name='create_checkout_session'),

    # Route for thank you on checkout success
    path('thank-you/', views.checkout_success, name='checkout_success'),

    # Route for webhook
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
]