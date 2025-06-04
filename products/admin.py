from django.contrib import admin
from .models import Service, Review





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

    # Fields shown in the service list view in the admin panel
    list_display = ('title', 'price', 'is_active', 'created_at')

    # Auto-fill the slug field based on the title input
    prepopulated_fields = {'slug': ('title',)}

    # Filters added to the right sidebar for admin filtering
    list_filter = ('is_active', 'created_at')

    # Allows the admin user to search services by title or description
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

    # Fields shown in the review list view
    list_display = ('service', 'user', 'rating', 'created_at')

    # Filters to help sort reviews by rating and date
    list_filter = ('rating', 'created_at')

    # Allows admin to search reviews by user or comment content
    search_fields = ('user__username', 'comment')
