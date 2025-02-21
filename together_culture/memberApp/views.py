from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is the index for members.")

def memberdashBoard(request):
    return render(request, 'memberDashboard.html')

def events(request):
    return render(request, 'events.html')

def benefits(request):
    return render(request, 'benefits.html')

def digitalContent(request):
    return render(request, 'digitalContent.html')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')