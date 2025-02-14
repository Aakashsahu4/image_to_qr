"""External Imports"""
from django.shortcuts import render

def login_view(request):
    return render(request, "login.html")

def signup_page(request):
    return render(request, 'signup.html')

def upload_page(request):
    return render(request, 'upload.html')

def images_page(request):
    return render(request, 'images.html')
