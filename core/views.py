from django.shortcuts import render

# =======================================================
# CORE VIEWS
# =======================================================

# Render the homepage using the base layout and the home.html template.
# This acts as the main landing page for the site.
def home(request):
    return render(request, 'core/home.html')
