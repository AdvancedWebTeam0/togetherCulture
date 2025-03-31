from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EventTag, EventLabel
from loginRegistrationApp.models import Events, Users, UserAttendingEvent, UserInterests
from memberApp.models import Membership
from .forms import EventSearchForm, UserSearchForm
import json
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.
# the url should be the name that is used in urls.py

nav_items = [
    {'name': 'Dashboard', 'url': 'admin-dashboard', 'submenu': None},
    {'name': '📊 Insights', 'url': 'insights', 'submenu': None},
    {'name': '📅 Manage Events', 'url': 'manage-events', 'submenu': None},
    {'name': '🔍 Search Users', 'url': 'user-list', 'submenu': None},
    {'name': '👥 Manage Members', 'url': '#', 'submenu': [
        {'name': '➕ Add Member', 'url': 'add-members'},
        {'name': '📋 Members List', 'url': 'members-list'},
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

    event_data = Events.objects.annotate(month=TruncMonth('eventDate')).values(
        'month').annotate(total=Count('eventId')).order_by('month')
    event_labels = [event['month'].strftime('%Y-%m') for event in event_data]
    data = [event['total'] for event in event_data]

    context = {'title': title,
               'nav_items': nav_items,
               'form': form,
               'tags': tags,
               'labels': labels,
               'cards': cards,
               'event_labels': json.dumps(event_labels),
               'data': json.dumps(data), }
    return render(request, 'admin_dashboard.html', context)


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
    tags = [int(tag) for tag in tags if tag.strip().isdigit()]
    labels = [int(label) for label in labels if label.strip().isdigit()]

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


def event_type_data(request):
    # Query to get event types and count
    event_type_data = (
        Events.objects.values('eventType')
        .annotate(event_count=Count('eventId'))
    )
    eventTypes = [event['eventType'] for event in event_type_data]
    eventTypeValues = [event['event_count'] for event in event_type_data]

    return JsonResponse({
        'eventTypes': eventTypes,
        'eventTypeValues': eventTypeValues
    })


def event_tag_data(request):
    # Query to get event tags and count
    event_tag_data = (
        EventTag.objects.values('eventTagName')
        .annotate(tag_count=Count('events'))
    )
    eventTags = [tag['eventTagName'] for tag in event_tag_data]
    eventTagValues = [tag['tag_count'] for tag in event_tag_data]

    return JsonResponse({
        'eventTags': eventTags,
        'eventTagValues': eventTagValues
    })


def event_label_data(request):
    # Query to get event labels and count
    event_label_data = (
        EventLabel.objects.values('eventLabelName')
        .annotate(label_count=Count('events'))
    )
    eventLabels = [label['eventLabelName'] for label in event_label_data]
    eventLabelValues = [label['label_count'] for label in event_label_data]

    return JsonResponse({
        'eventLabels': eventLabels,
        'eventLabelValues': eventLabelValues
    })


def insights(request):
    title = "Admin Insights"
    # Aggregating data from models for the insights page

    # Count total number of users
    num_users = Users.objects.count()

    # Count total number of events
    num_events = Events.objects.count()

    # Count total number of events attended
    num_attending_events = UserAttendingEvent.objects.filter(
        isUserAttended=True).count()

    # Count total number of user interests
    num_user_interests = UserInterests.objects.count()

    context = {
        'title': title,
        'nav_items': nav_items,
        'num_users': num_users,
        'num_events': num_events,
        'num_attending_events': num_attending_events,
        'num_user_interests': num_user_interests
    }

    return render(request, 'insights.html', context)


def events_per_month(request):
    # Get the current date
    now = timezone.now()

    # Get the first day of the current year to limit the query
    first_day_of_year = now.replace(month=1, day=1)
    
    # Aggregate the number of events per month for the current year
    events_per_month = (
        Events.objects.filter(eventDate__gte=first_day_of_year)
        .annotate(month=ExtractMonth('eventDate'))
        .values('month')
        .annotate(event_count=Count('eventId'))
        .order_by('month')
    )

    # Prepare labels for the chart (Months)
    months = [calendar.month_name[i] for i in range(1, 13)]

    # Prepare data for the chart
    event_counts = [0] * 12  # Default to 0 events for each month
    for event in events_per_month:
        event_counts[event['month'] - 1] = event['event_count']

    # Return JSON response
    return JsonResponse({
        'months': months,
        'event_counts': event_counts
    })


def event_search_date(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX Request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            # Convert to timezone-aware datetime
            start_date = timezone.make_aware(
                timezone.datetime.strptime(start_date, "%Y-%m-%d"))
            end_date = timezone.make_aware(
                timezone.datetime.strptime(end_date, "%Y-%m-%d"))

            events = Events.objects.filter(
                eventDate__range=[start_date, end_date]).order_by('eventDate')

            data = []
            for event in events:
                attendees = Users.objects.filter(
                    user_id__in=UserAttendingEvent.objects.filter(
                        event=event).values_list('user_id', flat=True)
                )

                event_data = {
                    'eventName': event.eventName,
                    'eventDate': event.eventDate.strftime('%Y-%m-%d'),
                    'location': event.location,
                    'totalAttendees': attendees.count(),
                    'attendees': [{'name': f"{attendee.first_name} {attendee.last_name}", 'email': attendee.email} for attendee in attendees]
                }

                data.append(event_data)

            return JsonResponse({'events': data})


def event_data(request):
    events = Events.objects.all()
    event_list = []

    for event in events:
        # If eventDate is a string, convert it to a datetime object
        if isinstance(event.eventDate, str):
            event.eventDate = datetime.strptime(event.eventDate, '%Y-%m-%dT%H:%M:%S')
    
    for event in events:
        event_list.append({
            'title': event.eventName,
            'start': event.eventDate.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.eventDate.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.shortDescription,
            'location': event.location,
            'slug': event.eventSlug,
        })
    return JsonResponse(event_list, safe=False)

def event_detail(request, slug):
    title = "Event details"
    event = Events.objects.get(eventSlug=slug)
    
    context = {'title': title,
               'nav_items': nav_items,
               'cards': cards,
               'event': event
               }
    
    return render(request, 'event_detail.html', context)

def __get_users(user_type: str):
    user_list = Users.objects.filter(current_user_type = user_type)
    return user_list


def __get_user_search_result(user_type: str, searched_string: str):
    # Using __icontains to search for names without case sensitivity and allow partial matches.
    results = Users.objects.filter(first_name__icontains=searched_string, current_user_type=user_type) | \
                    Users.objects.filter(last_name__icontains=searched_string, current_user_type=user_type) | \
                    Users.objects.filter(user_name__icontains=searched_string, current_user_type=user_type)
    return results


def members_list(request):
    title = "Members List"
    
    curr_members = __get_users(user_type = "MEMBER")
    curr_members_info = []

    for member in curr_members:
        curr_member_membership = Membership.objects.get(user = member, active = True)
        member_info = {
            'first_name': member.first_name,
            'last_name': member.last_name,
            'membership_type': curr_member_membership.membership_type,
            'slug': member.userSlug,
        }
        curr_members_info.append(member_info)

    context = {
        'title': title,
        'nav_items': nav_items,
        'form': UserSearchForm(),
        'members': curr_members_info,
    }
    return render(request=request, template_name='members_list.html', context=context)


def member_detail_view(request, slug):
    title = "Member Information"

    clicked_member = get_object_or_404(Users, userSlug=slug)
    clicked_member_curr_membership = Membership.objects.get(user = clicked_member, active = True)
    clicked_member_memberships = Membership.objects.filter(user = clicked_member)

    clicked_member_membership_history = []

    for history in clicked_member_memberships:
        history_item = {
            'membership_type': history.membership_type,
            'start_date': history.start_date,
            'end_date': history.end_date,
        }
        clicked_member_membership_history.append(history_item)

    member_info = {
        'first_name': clicked_member.first_name,
        'last_name': clicked_member.last_name,
        'user_name': clicked_member.user_name,
        'user_type': clicked_member.current_user_type,
        'have_interest_membership': clicked_member.have_interest_membership,
        'address': clicked_member.address,
        'email': clicked_member.email,
        'phone_number': clicked_member.phone_number,
        'gender': clicked_member.gender,
        'date_of_birth': clicked_member.date_of_birth,
        'profile_picture': clicked_member.profile_picture,
        'membership_type': clicked_member_curr_membership.membership_type,
        'membership_history': clicked_member_membership_history,
    }

    context = {
        'title': title,
        'nav_items': nav_items,
        'member': member_info,
    }

    return render(request=request, template_name='member_details.html', context=context)


def member_search(request):
    title = "Members List"

    context = {
                'title': title,
                'nav_items': nav_items,
                'form': UserSearchForm(),
            }

    if request.method == "GET":
        member_search_form = UserSearchForm(request.GET)

        if member_search_form.is_valid():
            memberString = member_search_form.cleaned_data['user']

            search_detail = "Search results for: \t" + memberString
            results = __get_user_search_result(user_type="MEMBER", searched_string=memberString)

            results_members_info = []
            for member in results:
                curr_member_membership = Membership.objects.get(user = member, active = True)

                member_info = {
                    'first_name': member.first_name,
                    'last_name': member.last_name,
                    'membership_type': curr_member_membership.membership_type,
                    'slug': member.userSlug,
                }
                results_members_info.append(member_info)
            
            context = {
                'title': title,
                'nav_items': nav_items,
                'form': UserSearchForm(),
                'members': results_members_info,
                'search_detail': search_detail,
            }

    return render(request=request, template_name='members_list.html', context=context)


def user_list(request):
    title = "User Search"
    
    curr_members = __get_users(user_type = "MEMBER")
    curr_nonmembers = __get_users(user_type = "NORMAL_USER")
    curr_users = curr_members | curr_nonmembers
    curr_users_info = []

    for user in curr_users:
        user_info = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.current_user_type,
            'slug': user.userSlug,
        }
        curr_users_info.append(user_info)

    context = {
        'title': title,
        'nav_items': nav_items,
        'form': UserSearchForm(),
        'users': curr_users_info,
    }

    return render(request=request, template_name='search_users.html', context=context)


def user_search(request):
    title = "User Search"

    context = {
                'title': title,
                'nav_items': nav_items,
                'form': UserSearchForm(),
            }

    if request.method == "GET":
        user_search_form = UserSearchForm(request.GET)

        if user_search_form.is_valid():
            userString = user_search_form.cleaned_data['user']
            membership_type = None
            search_detail = "Search results for: \t" + userString

            results_members = __get_user_search_result(user_type="MEMBER", searched_string=userString)
            results_nonmembers = __get_user_search_result(user_type="NORMAL_USER", searched_string=userString)
            results = results_members | results_nonmembers 

            results_users_info = []
            for user in results:
                user_info = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.current_user_type,
                    'slug': user.userSlug,
                }
                results_users_info.append(user_info)

            context = {
                'title': title,
                'nav_items': nav_items,
                'form': UserSearchForm(),
                'users': results_users_info,
            }

    return render(request=request, template_name='search_users.html', context=context)


def user_attending_event_view(request, slug):
    title = "User Information"

    clicked_user = get_object_or_404(Users, userSlug=slug)
    clicked_user_curr_membership = None

    if clicked_user.current_user_type == "MEMBER":
        clicked_user_curr_membership = Membership.objects.get(user = clicked_user, active = True).membership_type

    events_history = UserAttendingEvent.objects.filter(user = clicked_user)
    events_booked = []
    for entry in events_history:
        curr_event = entry.event
        event_info = {
            'eventName': curr_event.eventName,
            'eventDate': curr_event.eventDate,
            'location': curr_event.location,
            'eventType': curr_event.get_eventType_display(),
            'isUserAttended': entry.isUserAttended,
        }

        events_booked.append(event_info)

    user_info = {
        'first_name': clicked_user.first_name,
        'last_name': clicked_user.last_name,
        'user_name': clicked_user.user_name,
        'user_type': clicked_user.current_user_type,
        'membership_type': clicked_user_curr_membership,
        'events_booked': events_booked,
        'slug': clicked_user.userSlug,
    }

    context = {
                'title': title,
                'nav_items': nav_items,
                'form': UserSearchForm(),
                'user': user_info,
    }

    return render(request=request, template_name='details_user_attending_event.html', context=context)


def manage_events(request):
    # define the title for page
    title = "Manage Events"
    return render(request, 'manage_events.html', {'title': title, 'nav_items': nav_items})


def add_members(request):
    # define the title for page
    title = "Add Members"
    return render(request, 'add_members.html', {'title': title, 'nav_items': nav_items})


def manage_membership(request):
    # define the title for page
    title = "Manage Membership"
    return render(request, 'manage_membership.html', {'title': title, 'nav_items': nav_items})
