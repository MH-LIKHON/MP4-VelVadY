from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser





# =======================================================
# REGISTER CUSTOM USER MODEL IN DJANGO ADMIN
# =======================================================

# Customises the admin panel interface for the CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Specifies the fields displayed in the list view of the admin panel
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")

    # Adds filters for quick navigation in the admin panel
    list_filter = ("is_staff", "is_active")

    # Enables search functionality for these fields
    search_fields = ("email", "first_name", "last_name")

    # Orders the user list by email by default
    ordering = ("email",)

    # Defines field layout for editing user entries
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "address")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login",)}),
    )

    # Defines the layout when adding a new user via the admin interface
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "address",
                "password1", "password2", "is_staff", "is_active"
            )}
        ),
    )

# Registers the custom user model to appear in the Django admin panel
admin.site.register(CustomUser, CustomUserAdmin)