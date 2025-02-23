from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

nav_items = [
        {'name': '📊 Insights', 'url': 'insights', 'submenu': None},
        {'name': '📅 Events', 'url': 'events', 'submenu': None},
        {'name': '👥 Manage Members', 'url': 'manage-member/', 'submenu': [
            {'name': '➕ Add Member', 'url': 'add-member'},
            {'name': '📋 Members List', 'url': 'members-list'},
        ]},
        {'name': '🎟 Membership', 'url': 'membership/', 'submenu': None},
    ]
    

def index(request):
    return HttpResponse("Hello, world. This is the index for admin.")

def insights(request):
    # define the title for page
    title = "Insights"
    return render(request, 'insights.html', {'title': title, 'nav_items': nav_items})