import uuid
import logging
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Users, UserInterests, Interests
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from .forms import GetInitialInterest
from django.contrib import messages

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
            request.session['user_slug'] = user.userSlug  # Store userSlug in session
            request.session.modified = True  # Ensure session is saved
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
            # New Fields
            phone_number = request.POST.get('phone_number', '') 
            address = request.POST.get('address', '') 
            gender = request.POST.get('gender', '')  
            date_of_birth = request.POST.get('date_of_birth', None)
            
            # Generate a slug based on the user name
            userSlug = slugify(userName)

            # Ensure the slug is unique
            # If the slug already exists, you could append a number to make it unique
            slug_count = Users.objects.filter(userSlug=userSlug).count()
            if slug_count > 0:
                userSlug = f"{userSlug}-{slug_count + 1}"
        
            us = Users(
                user_id=userId,
                user_name=userName,
                first_name=firstName,
                last_name=lastName,
                email=email,
                password=password,
                current_user_type=currentUserType,
                have_interest_membership=haveInterestMembership,
                userSlug=userSlug,
                phone_number=phone_number,
                address=address,
                gender=gender,
                date_of_birth=date_of_birth
            )
            us.save()
            logger.info('User registered successfully')
            return redirect(getInitialInterests)
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
    request.session.flush()
    return render(request, 'Login.html')


def getInitialInterests(request):
    get_interests_form = GetInitialInterest()
    context = {
        'form': get_interests_form
    }

    if request.method == "POST":
        get_interests_form = GetInitialInterest(request.POST)
        if get_interests_form.is_valid():
            selected_options = get_interests_form.cleaned_data['interests']
            print("Selected Options:", selected_options)

            curr_user = Users.objects.first() #Update user!!
            response = __saveInitialInterests(user=curr_user, selected_options=selected_options)

            if response == "successfully saved":
                messages.success(request, "Interests saved successfully! Please log in to continue.")
                return redirect('login')
            
            else:
                messages.error(request, "Saving unsuccessful. Please try again.")
                return redirect(request.path)

    return render(request, 'get_interests.html', context=context)


def __saveInitialInterests(user:Users, selected_options:list):
    for interest in selected_options:
        curr_interest = Interests.objects.get(name=interest)
        user_interest = UserInterests(user= user, interest=curr_interest)
        user_interest.save()  # This will save the data to the database

    return "successfully saved"
