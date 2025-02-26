from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
# the url should be the name that is used in urls.py

nav_items = [
        {'name': 'Dashboard', 'url': 'admin-dashboard', 'submenu': None},
        {'name': '📊 Insights', 'url': 'insights', 'submenu': None},
        {'name': '📅 Manage Events', 'url': 'manage-events', 'submenu': None},
        {'name': '👥 Manage Members', 'url': '#', 'submenu': [
            {'name': '➕ Add Member', 'url': 'add-members'},
            {'name': '📋 Members List', 'url': 'manage-members'},
        ]},
        {'name': '🎟 Membership', 'url': 'manage-membership', 'submenu': None},
    ]
    
cards = [
        {"id": 1, "title": "Total Events", "value": 120, "footer": "Updated 2 hours ago"},
        {"id": 2, "title": "Active Tags", "value": 45, "footer": "Updated 3 hours ago"},
        {"id": 3, "title": "Upcoming Events", "value": 15, "footer": "Updated 5 hours ago"}
    ]

def admin_dashboard(request):
    # define the title for page
    title = "Admin Dashboard"
    return render(request, 'admin_dashboard.html', {'title': title, 
                                                    'nav_items': nav_items, 
                                                    'cards': cards})
    
def update_card(request, card_id):
    # Simulate fetching the updated value for the card from the database
    if card_id == '1':
        new_value = 130  # Updated value for card 1
    elif card_id == '2':
        new_value = 50   # Updated value for card 2
    elif card_id == '3':
        new_value = 200   # Updated value for card 3
    else:
        return JsonResponse({'error': 'Invalid card ID'}, status=400)
    
    # Return the updated value for the card
    return JsonResponse({'new_value': new_value})

def insights(request):
    # define the title for page
    title = "Insights"
    return render(request, 'insights.html', {'title': title, 'nav_items': nav_items})

def manage_events(request):
    # define the title for page
    title = "Manage Events"
    return render(request, 'manage_events.html', {'title': title, 'nav_items': nav_items})

def add_members(request):
    # define the title for page
    title = "Add Members"
    return render(request, 'add_members.html', {'title': title, 'nav_items': nav_items})

def manage_members(request):
    # define the title for page
    title = "Manage Members"
    return render(request, 'manage_members.html', {'title': title, 'nav_items': nav_items})

def manage_membership(request):
    # define the title for page
    title = "Manage Membership"
    return render(request, 'manage_membership.html', {'title': title, 'nav_items': nav_items})