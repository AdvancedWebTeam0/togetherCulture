from django.shortcuts import render, get_object_or_404
from .models import DigitalContentModule, ModuleBooking, Membership, Benefit, MembershipType
from loginRegistrationApp.models import Users
from django.core.paginator import Paginator
from django.http import JsonResponse

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


def profile(request):
    return render(request, 'profile.html')


def settings(request):
    return render(request, 'settings.html')
