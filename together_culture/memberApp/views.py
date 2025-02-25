from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is the index for members.")

def memberdashBoard(request):
    return render(request, 'memberDashboard.html')

def events(request):
    return render(request, 'events.html')

def benefits(request):
    return render(request, 'benefits.html')

def digitalContent(request):
    return render(request, 'digitalContent.html')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

#Will be deleted later, only written to adjust functionality.
def getInitialInterests(request):
    return render(request, 'get_interests.html')

def saveInitialInterests(request):
    return HttpResponse("Request is here")

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
