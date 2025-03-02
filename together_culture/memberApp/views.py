from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
import json
from .models import UserInterests


nav_items = [
        {'name': '🎟 My Membership', 'url': 'member-dashboard', 'submenu': None},
        {'name': '🎁 My Benefits', 'url': 'benefits', 'submenu': None},
        {'name': '📅 Events', 'url': 'events', 'submenu': None},
        {'name': '📚 Digital Content', 'url': 'digital-content', 'submenu': None},
        {'name': '👤 My Profile', 'url': 'profile', 'submenu': None},
        {'name': '⚙ Settings', 'url': 'settings', 'submenu': None},
    ]


# Create your views here.

def member_dashboard(request):
    title = 'Member Dashboard'
    return render(request, 'member_dashboard.html', {'title': title, 'nav_items': nav_items})

def events(request):
    return render(request, 'events.html')

def benefits(request):
    title = 'Benefits'
    return render(request, 'benefits.html', {'title': title, 'nav_items': nav_items})

def digital_content(request):
    title = 'Digital Content'
    return render(request, 'digital_content.html', {'title': title, 'nav_items': nav_items})

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

#Will be deleted later, only written to adjust functionality.
def getInitialInterests(request):
    return render(request, 'get_interests.html')

def saveInitialInterests(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            interests = data.get("interests", [])  # Extract list from request
            for interest in interests:
                curr_initial_interest = UserInterests(userId= 0, interestId=interest['id']) #update user id!
                curr_initial_interest.save()  # This will save the data to the database

            return JsonResponse({"message": "success"})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)