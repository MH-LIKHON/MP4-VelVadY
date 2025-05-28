from django.contrib import admin
from django.urls import path, include

# =======================================================
# ROOT PROJECT URLS
# =======================================================

# This file defines the project-level routing and includes app-specific URLs.
# I am currently linking to the core app and accounts app.

urlpatterns = [
    # Admin panel route
    path('admin/', admin.site.urls),

    # Route all base URLs to the core app (handles homepage and static pages)
    path('', include('core.urls')),

    # Route all /accounts/ URLs to the accounts app
    path('accounts/', include('accounts.urls')),
]