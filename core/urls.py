from django.urls import path
from . import views

# Linking the homepage URL to the view I just wrote in views.py
# This should route the root URL (empty path) to the home function.
urlpatterns = [
    path('', views.home, name='home'),
]