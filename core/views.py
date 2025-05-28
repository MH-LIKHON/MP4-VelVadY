from django.shortcuts import render

# This view now renders the homepage using the base layout and home.html
def home(request):
    return render(request, 'core/home.html')
