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

def validate_user(request):
    email = request.GET['email']
    password = request.GET['password']
    try:
        user = Users.objects.get(email=email)
        if check_password(password, user.password):
            logger.info('User authenticated successfully. User Email: ' + email)
            return redirect('/member')
        else:
            logger.warning('User authentication failed. User Email: ' + email)
            return JsonResponse({'statusCode': 401, 'message': 'User authentication failed. Wrong Password!'}, status=401)
    except Users.DoesNotExist:
        logger.warning('User does not exist. User Email: ' + email)
        return JsonResponse({'statusCode': 404, 'message': 'User with this email does not exist. Please click on Register.'}, status=404)
    except Exception as e:
        logger.error(f'Unexpected error during login: {e}')
        return JsonResponse({'statusCode': 500, 'message': f'Unexpected error during login: {e}'}, status=500)

def insert_user(request):
    if request.method == 'POST':
        try:
            userId = uuid.uuid4()
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            userName = firstName + "$" + lastName
            email = request.POST['email']
            password = make_password(request.POST['password'])
            currentUserType = "NORMAL_USER"
            haveInterestMembership = request.POST.get('terms') == 'on'

            us = Users(
                user_id=userId,
                user_name=userName,
                first_name=firstName,
                last_name=lastName,
                email=email,
                password=password,
                current_user_type=currentUserType,
                have_interest_membership=haveInterestMembership
            )
            us.save()
            logger.info('User registered successfully')
            return redirect('http://127.0.0.1:8000/')
        except Exception as e:
            logger.error(f'User registration failed: {e}')
            return JsonResponse({'statusCode': 500, 'message': 'User registration failed: User with this email already exists.'}, status=500)

def dashBoard(request):
    return render(request, 'Dashboard.html')

def manage_member(request):
    return render(request, 'manage_member.html')

def membership(request):
    return render(request, 'membership.html')

def logout(request):
    return render(request, 'Login.html')