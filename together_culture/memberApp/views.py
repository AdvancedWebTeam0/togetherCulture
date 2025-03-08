from django.shortcuts import render, redirect, get_object_or_404
from .models import DigitalContentModule, ModuleBooking
from django.http import JsonResponse
from loginRegistrationApp.models import Users

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
    return render(request, 'benefits.html', {'title': title, 'nav_items': nav_items})


def digital_content(request):
    title = 'Digital Content'
    # user2 = Users.objects.create(
    #     user_id="3", user_name="testuser1", first_name="John", last_name="Doe",
    #     email="johna`a@example.com", password="password", current_user_type="Admin"
    # )
    modules = DigitalContentModule.objects.all()
    return render(request, 'digital_content.html', {'title': title, 'nav_items': nav_items, 'modules': modules})


def book_module(request, module_id):
    request.user = Users.objects.get(user_id=3)
    if request.method == 'POST':
        user = request.user  # Get the logged-in user
        module = get_object_or_404(DigitalContentModule, pk=module_id)

        # Check if the user has already booked the module
        if ModuleBooking.objects.filter(user=user, module=module, is_booked=True).exists():
            return JsonResponse({'status': 'error', 'message': 'You have already booked this module.'})

        # Create a booking for the user
        ModuleBooking.objects.create(user=user, module=module, is_booked=True)
        return JsonResponse({'status': 'success', 'message': 'You have successfully booked the module!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def profile(request):
    return render(request, 'profile.html')


def settings(request):
    return render(request, 'settings.html')
