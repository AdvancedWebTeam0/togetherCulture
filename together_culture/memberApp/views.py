from django.shortcuts import render, get_object_or_404
from .models import DigitalContentModule, ModuleBooking, Membership, Benefit, MembershipType
from loginRegistrationApp.models import Users
from django.core.paginator import Paginator
from django.http import JsonResponse
from loginRegistrationApp.models import UserTypes
from django.shortcuts import render, redirect
from datetime import datetime
from memberApp.models import Membership, MembershipType, Benefit
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from loginRegistrationApp.models import Events, UserAttendingEvent

nav_items = [
    {'name': '🎟 Dashboard', 'url': 'member-dashboard', 'submenu': None},
    {'name': '🎁 My Benefits', 'url': 'benefits', 'submenu': None},
    {'name': '📅 Events', 'url': 'events', 'submenu': None},
    {'name': '📚 Digital Content', 'url': 'digital-content', 'submenu': None},
    {'name': '👤 My Membership', 'url': 'my_membership', 'submenu': None},
    {'name': '⚙ Settings', 'url': 'settings', 'submenu': None},
]

# Create your views here.


def member_dashboard(request):
    title = 'Member Dashboard'
    return render(request, 'member_dashboard.html', {'title': title, 'nav_items': nav_items})


def events(request):
    events_list = Events.objects.all()
    print("Fetched Events:", events_list)  # Debugging
    return render(request, 'events.html', {'events': events_list, 'title': 'Events', 'nav_items': nav_items})

def benefits(request):
    title = 'Benefits'
    request.user = Users.objects.get(
        user_id="d8ac4feb-e18a-4107-9df4-7aa093f38603")  # temp
    user = request.user
    benefits = Benefit.objects.filter(membership__user=user)
    membership_types = MembershipType.objects.all()  # Fetch all available plans

    return render(request, 'benefits.html', {'title': title, 'nav_items': nav_items,
                                             'benefits': benefits, 'membership_types': membership_types})


def use_benefit(request, benefit_id):
    request.user = Users.objects.get(
        user_id="d8ac4feb-e18a-4107-9df4-7aa093f38603")  # temp
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
        user_id="d8ac4feb-e18a-4107-9df4-7aa093f38603")  # temp
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
    return render(request, 'settings.html')

def buy_membership(request):
    user_slug = request.session.get("user_slug")  # Get user_slug from session
    if not user_slug:
        return redirect('/loginRegistration/login/')  # Redirect if not logged in

    try:
        user = Users.objects.get(userSlug=user_slug)
    except Users.DoesNotExist:
        request.session.flush()  # Ensure session is cleared if the user does not exist
        return redirect('/loginRegistration/login/')

    if request.method == "GET":
        latest_membership = UserTypes.objects.filter(user=user).order_by('-date').first()
        current_membership = latest_membership.userType if latest_membership else None

        return render(request, "buy_membership.html", {
            'current_membership': current_membership
        })

    if request.method == "POST":
        membership_type_name = request.POST.get("membership_type")
        if not membership_type_name:
            return JsonResponse({'statusCode': 400, 'message': 'Membership type is required'}, status=400)

        try:
            membership_type = MembershipType.objects.get(name=membership_type_name)
        except MembershipType.DoesNotExist:
            return JsonResponse({'statusCode': 404, 'message': 'Invalid membership type'}, status=404)

        try:
            # Set previous memberships as inactive
            Membership.objects.filter(user=user, active=True).update(active=False)

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
            UserTypes.objects.create(user=user, userType=membership_type.name, date=datetime.now())

            return JsonResponse({'statusCode': 200, 'message': 'Membership purchased successfully'})

        except Exception as e:
            return JsonResponse({'statusCode': 500, 'message': f'Unexpected error: {e}'}, status=500)

    return JsonResponse({'statusCode': 405, 'message': 'Method not allowed'}, status=405)



# @csrf_exempt  # Only if necessary
# def book_event(request):
#     if request.method != "POST":
#         return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

#     try:
#         # Parse the JSON data from the request body
#         data = json.loads(request.body.decode("utf-8"))
#         print("Received data:", data)  # Debugging output

#         # Get eventId from the data
#         event_id = data.get("eventId")
#         print("Event ID:", event_id)  # Debugging output

#         if not event_id:
#             return JsonResponse({"status": "error", "message": "Missing event ID"}, status=400)

#         user_slug = request.session.get("user_slug")
#         if not user_slug:
#             return JsonResponse({"status": "error", "message": "User not logged in or session expired."}, status=401)

#         user = get_object_or_404(Users, userSlug=user_slug)
        
#         # Important: Use eventId here, not id
#         event = get_object_or_404(Events, eventId=event_id)

#         # Avoid duplicate bookings
#         attending, created = UserAttendingEvent.objects.get_or_create(
#             user=user,
#             event=event,
#             defaults={"isUserAttended": False}  # Set default value
#         )

#         if created:
#             # Only increment if this is a new booking
#             event.numberOfAttendees += 1
#             event.save()
#             print(f"User {user.userSlug} booked event {event.eventName}, new attendance count: {event.numberOfAttendees}")
#         else:
#             print(f"User {user.userSlug} already booked event {event.eventName}")

#         return JsonResponse({
#             "status": "success",
#             "message": "Event booked successfully!",
#             "attendees": event.numberOfAttendees
#         })

#     except json.JSONDecodeError as e:
#         print("JSON Decode Error:", str(e))
#         return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

#     except Exception as e:
#         print("Unexpected error:", str(e))
#         return JsonResponse({"status": "error", "message": f"Unexpected error: {e}"}, status=500)

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