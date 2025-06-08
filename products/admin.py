from django.contrib import admin
from .models import Service, Review, Purchase


# =======================================================
# ADMIN DISPLAY FOR SERVICE MODEL
# =======================================================

# Handles admin display of digital services
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Custom admin display configuration for the Service model.
    This enables sorting, searching, and auto-generating slugs in the admin panel.
    """
    list_display = ('title', 'price', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')


# =======================================================
# ADMIN DISPLAY FOR REVIEW MODEL
# =======================================================

# Handles admin display of reviews for services
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Custom admin display configuration for the Review model.
    Enables admin staff to view and manage submitted reviews easily.
    """
    list_display = ('service', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'comment')


# =======================================================
# ADMIN DISPLAY FOR PURCHASE MODEL
# =======================================================

# Handles admin display of completed purchases
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """
    Custom admin display configuration for the Purchase model.
    Displays key information about Stripe-based transactions.
    """
    list_display = ('user', 'service', 'amount_paid', 'stripe_session_id', 'timestamp')
    list_filter = ('service', 'timestamp')
    search_fields = ('stripe_session_id', 'user__email')
