from django.shortcuts import render
from django.http import HttpResponse
from loginRegistrationApp.models import Events

def events_view(request):
    # Fetch all events
    events = Events.objects.all()

    # Pass events to the template
    return render(request, 'event_view.html', {'events': events})

# Create your views here.

# def index(request):
#     return render(request, 'index.html')
# from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def event(request):
    events_list = [
        {'title': 'Event I'},
        {'title': 'Event II'},
        {'title': 'Event III'},
    ]

    events = Events.objects.all()

    # Pass events to the template
    return render(request, 'event.html', {'events': events})
    # return render(request, 'event.html', {'events': events_list})


# def membership(request):
#     return render(request, 'membership.html') 

def membership(request):
    membership_types = {
        'individual': [
            {'title': 'Community Membership', 'description': 'For community members'},
            {'title': 'Workspace Membership: Touchdown', 'description': 'Flexible workspace option'},
            {'title': 'Workspace Membership: Dedicated', 'description': 'Dedicated workspace option'},
        ],
        'organizational': []
    }
    return render(request, 'membership.html', {'membership_types': membership_types})

def about(request):
    return render(request, 'about.html')

def resources(request):
    return render(request, 'resources.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')