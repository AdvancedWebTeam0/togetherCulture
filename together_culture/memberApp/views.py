from django.shortcuts import render, get_object_or_404
from .models import DigitalContentModule, ModuleBooking, Membership, Benefit, MembershipType
from loginRegistrationApp.models import Users
from django.core.paginator import Paginator
from django.http import JsonResponse
from loginRegistrationApp.models import UserTypes, UserInterests, UserAttendingEvent, Events, Interests
from django.shortcuts import render, redirect
from datetime import datetime
from memberApp.models import Membership, MembershipType, Benefit
from datetime import datetime, timedelta
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

    user = Users.objects.get(userSlug="ela_dogruyol") #Needs to change. Will get the user_slug from session.

    total_num_of_events, in_interests_events, not_in_interests_events, activity_count_dict_interest, activity_count_dict_others = __get_interest_event_data(user=user)

    context = {
        'title': title,
        'nav_items': nav_items,
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


def events(request):
    return render(request, 'events.html')


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
