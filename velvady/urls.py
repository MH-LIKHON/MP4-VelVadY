from core import views
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.conf.urls.static import static

# =======================================================
# ROOT PROJECT URLS
# =======================================================

# This file defines the project level routing and includes app specific URLs
urlpatterns = [

    # Route all base URLs to the core app (handles homepage and static pages)
    path('', include('core.urls')),

    # Route to admin
    path('admin/', admin.site.urls),

    # Route to accounts
    path('accounts/', include('accounts.urls')),

    # Route to products
    path("products/", include("products.urls")),
]





# =======================================================
# MEDIA FILE SERVING DURING DEVELOPMENT
# =======================================================

# This block allows Django to serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# =======================================================
# CUSTOM ERROR HANDLERS
# =======================================================
    
# Route to 404
handler404 = 'core.views.custom_404'