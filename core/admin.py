from django.contrib import admin
from .models import ContactMessage





# =======================================================
# ADMIN DISPLAY FOR CONTACT MESSAGES
# =======================================================

# Shows submitted contact messages in the admin interface
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for displaying contact messages.
    Allows admin to view who submitted what and when.
    """

    # Fields shown in the list view
    list_display = ('name', 'email', 'submitted_at')

    # Filters for quick sorting in the right-hand panel
    list_filter = ('submitted_at',)

    # Enable search by name and email
    search_fields = ('name', 'email')