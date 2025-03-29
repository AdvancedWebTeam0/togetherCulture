from django.shortcuts import render, get_object_or_404
from .models import DigitalContentModule, ModuleBooking, Membership, Benefit, MembershipType
from loginRegistrationApp.models import Users
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from loginRegistrationApp.models import UserTypes, UserAttendingEvent, Events
from django.shortcuts import render, redirect
from datetime import datetime
from memberApp.models import Membership, MembershipType, Benefit
from datetime import datetime, timedelta
from django.http import Http404

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
    #username = request.user.user_name
    user = request.user = Users.objects.get(
        user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a")  # temp
    username = request.user.user_name
    
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
        'username': username,
        'membership_type': membership_type,
        'start_date': membership.start_date,
        'end_date': membership.end_date
    }

    return render(request, 'member_dashboard.html', context)


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
    return render(request, 'events.html')

# @login_required


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
    return render(request, 'settings.html')


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
