from django.urls import path
from . import views

# =======================================================
# URL PATTERNS FOR PRODUCTS APP
# =======================================================

# This file defines the routes
urlpatterns = [

    # This URL shows all active services in a grid layout
    path('services/', views.product_list_view, name='product_list'),

    # This URL displays a specific service based on its slug
    path('<slug:slug>/', views.service_detail_view, name='service_detail'),
]