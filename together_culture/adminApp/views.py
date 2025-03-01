from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EventTag, EventLabel
from loginRegistrationApp.models import Events, Users
from .forms import EventSearchForm
import json
from django.utils import timezone
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
    {'id': 1, 'title': 'Total number of members',
        'value': 0, 'interval': 10000},  # 10 seconds
    {'id': 2, 'title': 'Number of upcoming events', 'value': 0, 'interval': 10000},
    {'id': 3, 'title': 'Total number of tags', 'value': 0, 'interval': 90000},
    {'id': 4, 'title': 'Total number of labels', 'value': 0, 'interval': 90000},
]


def admin_dashboard(request):
    # define the title for page
    title = "Admin Dashboard"

    # Retrieve all tags and labels to display in the form
    tags = EventTag.objects.all()
    labels = EventLabel.objects.all()

    form = EventSearchForm(request.GET)  # Prefill form with GET data if any

    return render(request, 'admin_dashboard.html', {'title': title,
                                                    'nav_items': nav_items,
                                                    'form': form,
                                                    'tags': tags,
                                                    'labels': labels,
                                                    'cards': cards})


def update_card(request, card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid card ID'}, status=400)
    # Simulate fetching the updated value for the card from the database
    if card_id == 1:
        new_value = Users.objects.filter(current_user_type='member').count()
    elif card_id == 2:
        current_time = timezone.now()
        new_value = Events.objects.filter(eventDate__gt=current_time).count()
    elif card_id == 3:
        new_value = EventTag.objects.count()
    elif card_id == 4:
        new_value = EventLabel.objects.count()
    else:
        return JsonResponse({'error': 'Invalid card ID'}, status=400)
    # Return the updated value for the card
    return JsonResponse({'new_value': new_value})


def save_tag(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))
            tag_name = data.get('tag_name')

            # If a tag name is provided, create a new tag
            if tag_name:
                new_tag = EventTag.objects.create(eventTagName=tag_name)
                return JsonResponse({'success': True, 'tag': new_tag.eventTagName})
            else:
                return JsonResponse({'success': False, 'error': 'No tag name provided'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests with JSON data are allowed'})


def save_label(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))
            label_name = data.get('label_name')

            # If a label name is provided, create a new label
            if label_name:
                new_label = EventLabel.objects.create(
                    eventLabelName=label_name)
                return JsonResponse({'success': True, 'label': new_label.eventLabelName})
            else:
                return JsonResponse({'success': False, 'error': 'No label name provided'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests with JSON data are allowed'})


def event_search(request):

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request, must be AJAX.'}, status=400)

    # Preprocess GET data to split comma-separated values
    tags = request.GET.get('tags', '').split(',')
    labels = request.GET.get('labels', '').split(',')

    # Convert string values to integers (if they are supposed to be IDs)
    try:
        tags = [int(tag) for tag in tags if tag.strip().isdigit()]
        labels = [int(label) for label in labels if label.strip().isdigit()]
    except ValueError:
        return JsonResponse({'error': 'Invalid tag or label ID'}, status=400)

    # Rebuild the GET data with properly split values
    request.GET = request.GET.copy()
    request.GET.setlist('tags', tags)
    request.GET.setlist('labels', labels)

    # Initialize form with the corrected GET data
    form = EventSearchForm(request.GET)

    # Check if the form is valid and the request is AJAX
    if form.is_valid():
        tags = form.cleaned_data.get('tags', [])
        labels = form.cleaned_data.get('labels', [])

        events = Events.objects.all()

        if tags:
            events = events.filter(tags__in=tags).distinct()
        if labels:
            events = events.filter(labels__in=labels).distinct()

        # If no events are found, return an error message
        if not events.exists():
            return JsonResponse({'error': 'No events found matching the criteria.'}, status=404)

        # Prepare event data for the response
        event_data = []
        for event in events:
            event_data.append({
                'title': event.eventName,
                'description': event.shortDescription,
                'tags': [tag.eventTagName for tag in event.tags.all()],
                'labels': [label.eventLabelName for label in event.labels.all()],
            })

        return JsonResponse({'events': event_data})

    # If form is not valid, return an error message
    return JsonResponse({'error': 'No events found matching the criteria.'}, status=404)


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
