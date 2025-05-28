from django.shortcuts import render

# Create your views here.



from django.http import HttpResponse

# Created a simple view here just to test if the project setup is working.
# This should return a plain message at the homepage URL.
def home(request):
    return HttpResponse("Welcome to VelVady!")