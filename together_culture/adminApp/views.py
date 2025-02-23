from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

nav_items = [
        {'name': '📊 Insights', 'url': '/home/', 'submenu': None},
        {'name': '📅 Events', 'url': '/about/', 'submenu': None},
        {'name': '👥 Manage Members', 'url': '#', 'submenu': [
            {'name': '➕ Add Member', 'url': '/services/web-design/'},
            {'name': '📋 Members List', 'url': '/services/seo/'},
        ]},
        {'name': '🎟 Membership', 'url': '/contact/', 'submenu': None},
    ]
    

def index(request):
    return HttpResponse("Hello, world. This is the index for admin.")

def insights(request):
    # define the title for page
    title = "Insights"
    return render(request, 'insights.html', {'title': title, 'nav_items': nav_items})