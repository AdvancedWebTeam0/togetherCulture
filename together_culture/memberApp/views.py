from django.shortcuts import render, get_object_or_404
from .models import DigitalContentModule, ModuleBooking, Membership, Benefit, MembershipType
from loginRegistrationApp.models import Users
from django.core.paginator import Paginator
from django.http import JsonResponse
from loginRegistrationApp.models import UserTypes, UserInterests, UserAttendingEvent, Events, Interests
from django.contrib.auth.decorators import login_required
from loginRegistrationApp.models import UserTypes, UserAttendingEvent, Events
from django.shortcuts import render, redirect
from datetime import datetime
from memberApp.models import Membership, MembershipType, Benefit
from datetime import datetime, timedelta
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from loginRegistrationApp.models import Events, UserAttendingEvent
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password

nav_items = [
    {'name': '🎟 Dashboard', 'url': 'member-dashboard', 'submenu': None},
    {'name': '🎁 My Benefits', 'url': 'benefits', 'submenu': None},
    {'name': '📅 Events', 'url': 'events', 'submenu': None},
    {'name': '📚 Digital Content', 'url': 'digital-content', 'submenu': None},
    {'name': '👤 My Membership', 'url': 'my_membership', 'submenu': None},
    {'name': '⚙ Settings', 'url': 'settings', 'submenu': None},
]

# Create your views here.


# @login_required
def member_dashboard(request):
    title = 'Member Dashboard'
    user_slug = request.session.get('user_slug')
    user = Users.objects.get(userSlug=user_slug)
    #username = request.user.user_name
    # user = request.user = Users.objects.get(
    #     user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a")  # temp
    # username = request.user.user_name
    
    # Fetch the user's active membership
    membership = Membership.objects.filter(user=user, active=True).latest(
        'start_date')  # Get the latest active membership

    # Retrieve the membership type
    # Access the membership type (e.g., 'Premium', 'VIP', etc.)
    membership_type = membership.membership_type.name



    #user = Users.objects.get(userSlug="ela_dogruyol") #Needs to change. Will get the user_slug from session.
    total_num_of_events, in_interests_events, not_in_interests_events, activity_count_dict_interest, activity_count_dict_others = __get_interest_event_data(user=user)

    context = {
        'title': title,
        'nav_items': nav_items,
        'username': username,
        'membership_type': membership_type,
        'start_date': membership.start_date,
        'end_date': membership.end_date,
        'total_num_of_events': total_num_of_events,
        'in_interests_events': in_interests_events,
        'not_in_interests_events': not_in_interests_events,
        'activity_count_dict_interest': activity_count_dict_interest,
        'activity_count_dict_others': activity_count_dict_others,
    }

    return render(request=request, template_name='member_dashboard.html', context=context)


def __get_interest_event_data(user:Users):
    all_interests = Interests.objects.all()

    user_interests = UserInterests.objects.filter(user=user)

    curr_interests = []
    for user_interest in user_interests:
        curr_interests.append(user_interest.interest.name)

    booked_events = UserAttendingEvent.objects.filter(user=user)

    #get events list booked, with the separation of related to interests or not
    events_related_to_interests = []
    events_not_related_to_interests = []
    for entity in booked_events:
        curr_event = entity.event
        if curr_event.get_eventType_display() in curr_interests:
            events_related_to_interests.append(curr_event)
        else:
            events_not_related_to_interests.append(curr_event) 

    #get activity count for interests and other areas
    activity_count_dict_others = {}
    activity_count_dict_interests = {}
    for interest in all_interests:
        interest_name = interest.name
        event_count = 0

        for entity in booked_events:
            event_type = entity.event.get_eventType_display()
            if interest_name == event_type:
                event_count = event_count + 1

        if interest_name in curr_interests:
            activity_count_dict_interests[interest_name] = event_count
        else:
            activity_count_dict_others[interest_name] = event_count

    return len(booked_events), events_related_to_interests, events_not_related_to_interests, activity_count_dict_interests, activity_count_dict_others


def event_data(request):
    # Get the logged-in user
    user = request.user
    user = request.user = Users.objects.get(
        user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a")  # temp
    # Fetch the UserAttendingEvent records for the logged-in user where the user is attending
    user_events = UserAttendingEvent.objects.filter(
        user=user, isUserAttended=False)

    # Create the list of events the user is attending
    event_list = []
    for user_event in user_events:
        event = user_event.event  # Get the related Event from UserAttendingEvent

        # If eventDate is a string, convert it to a datetime object
        if isinstance(event.eventDate, str):
            event.eventDate = datetime.strptime(
                event.eventDate, '%Y-%m-%dT%H:%M:%S')

        # Add the event details to the event list
        event_list.append({
            'title': event.eventName,
            'start': event.eventDate.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.eventDate.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.shortDescription,
            'location': event.location,
            'slug': event.eventSlug,
        })
    print(event_list)
    # Return the filtered event list as a JSON response
    return JsonResponse(event_list, safe=False)

def event_detail(request, slug):
    title = "Event details"
    event = Events.objects.get(eventSlug=slug)

    context = {'title': title,
               'nav_items': nav_items,
               'event': event
               }

    return render(request, 'event_detail.html', context)


def events(request):
    events_list = Events.objects.all()
    print("Fetched Events:", events_list)  # Debugging
    return render(request, 'events.html', {'events': events_list, 'title': 'Events', 'nav_items': nav_items})

def benefits(request):
    title = 'Benefits'
    request.user = Users.objects.get(
        user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a")  # temp
    user = request.user
    benefits = Benefit.objects.filter(membership__user=user)

    # Fetch the user's active membership
    membership = Membership.objects.filter(user=user, active=True).latest(
        'start_date')  # Get the latest active membership

    # Retrieve the membership type
    # Access the membership type (e.g., 'Premium', 'VIP', etc.)
    membership_type = membership.membership_type.name

    # Create the context to pass to the template
    context = {
        'title': title,
        'nav_items': nav_items,
        'benefits': benefits,
        'membership_type': membership_type,
        'start_date': membership.start_date,
        'end_date': membership.end_date
    }

    return render(request, 'benefits.html', context)


def use_benefit(request, benefit_id):
    request.user = Users.objects.get(
        user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a")  # temp
    user = request.user

    # Get user's membership
    membership = Membership.objects.filter(user=user).first()
    if not membership:
        return JsonResponse({"success": False, "message": "No active membership found."})

    # Get the benefit associated with their membership
    benefit = get_object_or_404(Benefit, id=benefit_id, membership=membership)

    # Try to use the benefit
    if benefit.use_benefit():
        return JsonResponse({"success": True, "remaining": benefit.remaining()})
    else:
        return JsonResponse({"success": False, "message": "You have used up this benefit."})


def digital_content(request):
    title = 'Digital Content'

    modules = DigitalContentModule.objects.all().order_by('-module_id')

    # Pagination: We want to display 5 modules per page
    paginator = Paginator(modules, 5)  # Show 5 modules per page.

    # Get the page number from the request, default to 1
    # 'page' is the query parameter in the URL
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'digital_content.html', {'title': title, 'nav_items': nav_items,
                                                    'page_obj': page_obj})


def book_module(request, module_id):
    request.user = Users.objects.get(
        user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a")  # temp
    if request.method == 'POST':
        user = request.user  # Get the logged-in user
        module = get_object_or_404(DigitalContentModule, pk=module_id)

        # Check if the user has already booked the module
        if ModuleBooking.objects.filter(user=user, module=module, is_booked=True).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already booked this module.'})

        # Create a booking for the user
        ModuleBooking.objects.create(user=user, module=module, is_booked=True)

        # Get user's membership
        membership = Membership.objects.filter(user=user).first()
        if not membership:
            return JsonResponse({"status": 'error', 'message': "No active membership found."})

        benefit = get_object_or_404(Benefit, id=1, membership=membership)

        if benefit.use_benefit():
            return JsonResponse({'status': 'success', 'message': "You have successfully booked the module!"})
        else:
            return JsonResponse({'status': 'error', 'message': "You have used up this benefit."})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def my_membership(request):
    return redirect('buy_membership')


def settings(request):
    
    user_slug = request.session.get("user_slug")
    if not user_slug:
        messages.error(request, "User not logged in")
        return redirect('login')  # Redirect to login if session data is missing

    try:
        user = Users.objects.get(userSlug=user_slug)
        user_id = user.user_id
    except Users.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

    if request.method == 'POST':
        # Update user details from form submission
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        user.gender = request.POST.get('gender', user.gender)

        # Handle password reset fields
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if new_password or confirm_password:
            if new_password == confirm_password:
                user.password = make_password(new_password)
            else:
                messages.error(request, "New password and confirmation do not match.")
                return redirect('settings')

        # Update user_name and regenerate userSlug based on first and last name
        user.user_name = user.first_name + "$" + user.last_name
        new_slug = slugify(user.user_name)
        # Ensure the new slug is unique by checking other records
        slug_count = Users.objects.filter(userSlug=new_slug).exclude(user_id=user_id).count()
        if slug_count > 0:
            new_slug = f"{new_slug}-{slug_count + 1}"
        user.userSlug = new_slug

        user.save()
        # Update session variables if needed (e.g., user_slug)
        request.session['user_slug'] = user.userSlug

        messages.success(request, "Your details have been updated.")
        return redirect('settings')

    context = {
        'user': user,
    }
    return render(request, 'settings.html', context)


def buy_membership(request):
    user_slug = request.session.get("user_slug")  # Get user_slug from session
    if not user_slug:
        # Redirect if not logged in
        return redirect('/loginRegistration/login/')

    try:
        user = Users.objects.get(userSlug=user_slug)
    except Users.DoesNotExist:
        request.session.flush()  # Ensure session is cleared if the user does not exist
        return redirect('/loginRegistration/login/')

    if request.method == "GET":
        latest_membership = UserTypes.objects.filter(
            user=user).order_by('-date').first()
        current_membership = latest_membership.userType if latest_membership else None

        return render(request, "buy_membership.html", {
            'current_membership': current_membership
        })

    if request.method == "POST":
        membership_type_name = request.POST.get("membership_type")
        if not membership_type_name:
            return JsonResponse({'statusCode': 400, 'message': 'Membership type is required'}, status=400)

        try:
            membership_type = MembershipType.objects.get(
                name=membership_type_name)
        except MembershipType.DoesNotExist:
            return JsonResponse({'statusCode': 404, 'message': 'Invalid membership type'}, status=404)

        try:
            # Set previous memberships as inactive
            Membership.objects.filter(
                user=user, active=True).update(active=False)

            # Create a new membership entry
            new_membership = Membership.objects.create(
                user=user,
                membership_type=membership_type,
                start_date=datetime.today(),
                end_date=datetime.today() + timedelta(days=30),
                active=True
            )

            # Update user status to "MEMBER"
            user.current_user_type = "MEMBER"
            user.save()

            # Log user membership in UserTypes
            UserTypes.objects.create(
                user=user, userType=membership_type.name, date=datetime.now())

            return JsonResponse({'statusCode': 200, 'message': 'Membership purchased successfully'})

        except Exception as e:
            return JsonResponse({'statusCode': 500, 'message': f'Unexpected error: {e}'}, status=500)

    return JsonResponse({'statusCode': 405, 'message': 'Method not allowed'}, status=405)


@csrf_exempt  # Only if necessary
def book_event(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))
        print("Received data:", data)  # Debugging output

        # Get eventId from the data
        event_id = data.get("eventId")
        print("Event ID:", event_id)  # Debugging output

        if not event_id:
            return JsonResponse({"status": "error", "message": "Missing event ID"}, status=400)

        user_slug = request.session.get("user_slug")
        if not user_slug:
            return JsonResponse({"status": "error", "message": "User not logged in or session expired."}, status=401)

        user = get_object_or_404(Users, userSlug=user_slug)
        
        # Important: Use eventId here, not id
        event = get_object_or_404(Events, eventId=event_id)

        # Avoid duplicate bookings
        attending, created = UserAttendingEvent.objects.get_or_create(
            user=user,
            event=event,
            defaults={"isUserAttended": False}  # Set default value
        )

        if created:
            # Only increment if this is a new booking
            event.numberOfAttendees += 1
            event.save()
            print(f"User {user.userSlug} booked event {event.eventName}, new attendance count: {event.numberOfAttendees}")
            return JsonResponse({
                "status": "success",
                "message": "Event booked successfully!",
                "attendees": event.numberOfAttendees,
                "is_new_booking": True
            })
        else:
            print(f"User {user.userSlug} already booked event {event.eventName}")
            return JsonResponse({
                "status": "already_booked",
                "message": "You have already booked this event!",
                "attendees": event.numberOfAttendees,
                "is_new_booking": False
            })

    except json.JSONDecodeError as e:
        print("JSON Decode Error:", str(e))
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    except Exception as e:
        print("Unexpected error:", str(e))
        return JsonResponse({"status": "error", "message": f"Unexpected error: {e}"}, status=500)