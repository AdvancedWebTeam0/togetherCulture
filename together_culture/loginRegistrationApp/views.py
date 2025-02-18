import uuid
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Users
from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger('landing')

def login(request):
    return render(request, 'Login.html')

def register(request):
    return render(request, 'Register.html')

def validateUser(request):
    email = request.GET['email']
    password = request.GET['password']
    try:
        user = Users.objects.get(email=email)
        if check_password(password, user.password):
            logger.info('User authenticated successfully. User Email: ' + email)
            return redirect('dashboard')
        else:
            logger.warning('User authentication failed. User Email: ' + email)
            return JsonResponse({'statusCode': 401, 'message': 'User authentication failed. Wrong Password!'}, status=401)
    except User.DoesNotExist:
        logger.warning('User does not exist. User Email: ' + email)
        return JsonResponse({'statusCode': 404, 'message': 'User with this email does not exist. Please click on Register.'}, status=404)
    except Exception as e:
        logger.error(f'Unexpected error during login: {e}')
        return JsonResponse({'statusCode': 500, 'message': f'Unexpected error during login: {e}'}, status=500)

def insertUser(request):
    return render(request, 'Register.html')

def dashBoard(request):
    return render(request, 'Dashboard.html')


def insights(request):
    return render(request, 'insights.html')

def events(request):
    return render(request, 'events.html')

def manage_member(request):
    return render(request, 'manage_member.html')

def membership(request):
    return render(request, 'membership.html')