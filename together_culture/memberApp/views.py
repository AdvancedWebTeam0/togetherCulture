from django.shortcuts import render, redirect
from django.http import HttpResponse


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