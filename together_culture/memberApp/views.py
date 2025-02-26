from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse


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
    return render(request, 'digital_content.html', {'title': title, 'nav_items': nav_items})

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

#Will be deleted later, only written to adjust functionality.
def getInitialInterests(request):
    return render(request, 'get_interests.html')

def saveInitialInterests(request):
    data = {"message": "Success"}  # Ensure this is a dictionary
    return JsonResponse(data)

    email = request.GET['email']
    password = request.GET['password']
    '''try:
        user = Users.objects.get(email=email)
        if check_password(password, user.password):
            logger.info('User authenticated successfully. User Email: ' + email)
            return redirect('dashboard')
        else:
            logger.warning('User authentication failed. User Email: ' + email)
            return JsonResponse({'statusCode': 401, 'message': 'User authentication failed. Wrong Password!'}, status=401)
    except Users.DoesNotExist:
        logger.warning('User does not exist. User Email: ' + email)
        return JsonResponse({'statusCode': 404, 'message': 'User with this email does not exist. Please click on Register.'}, status=404)
    except Exception as e:
        logger.error(f'Unexpected error during login: {e}')
        return JsonResponse({'statusCode': 500, 'message': f'Unexpected error during login: {e}'}, status=500)'''
