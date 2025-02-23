from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

nav_items = [
        {'name': '🎟 My Membership', 'url': 'member-dashboard', 'submenu': None},
        {'name': '🎁 My Benefits', 'url': 'benefits', 'submenu': None},
        {'name': '📅 Events', 'url': 'events', 'submenu': None},
        {'name': '📚 Digital Content', 'url': 'digital-content', 'submenu': None},
        {'name': '👤 My Profile', 'url': 'profile', 'submenu': None},
        {'name': '⚙️ Settings', 'url': 'settings', 'submenu': None},
    ]

def member_dashboard(request):
    title = 'Member Dashboard'
    return render(request, 'member_dashboard.html', {'title': title, 'nav_items': nav_items})

def events(request):
    title = 'Events'
    return render(request, 'events.html', {'title': title, 'nav_items': nav_items})

def benefits(request):
    title = 'Benefits'
    return render(request, 'benefits.html', {'title': title, 'nav_items': nav_items})

def digital_content(request):
    title = 'Digital Content'
    return render(request, 'digital_content.html', {'title': title, 'nav_items': nav_items})

def profile(request):
    title = 'Profile'
    return render(request, 'profile.html', {'title': title, 'nav_items': nav_items})

def settings(request):
    title = 'Settings'
    return render(request, 'settings.html', {'title': title, 'nav_items': nav_items})