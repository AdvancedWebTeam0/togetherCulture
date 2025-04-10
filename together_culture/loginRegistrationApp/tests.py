from django.test import TestCase

import json
import uuid
from datetime import datetime, date

from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

# Import the views and models from your app.
# Adjust the import paths below to match your project structure.
from loginRegistrationApp.models import Users
from loginRegistrationApp.views import validate_user, insert_user

# For this example, we will define a dummy view function for getInitialInterests
# so that insert_user() can redirect to it.
def dummy_get_initial_interests(request):
    # In a real app this would be a proper view, here we simply return a 200 OK.
    from django.http import HttpResponse
    return HttpResponse("Interests Page")

# Patch the getInitialInterests used by insert_user to our dummy view.
import memberApp.views
memberApp.views.getInitialInterests = dummy_get_initial_interests


class ValidateUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create two users: one admin and one normal/membership user.
        self.admin_user = Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Admin.User@togetherculture.com",
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password=make_password("adminpass"),
            current_user_type="ADMIN",
            have_interest_membership=False,
            userSlug="admin-user"
        )
        self.normal_user = Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Normal.User@togetherculture.com",
            first_name="Normal",
            last_name="User",
            email="normal@example.com",
            password=make_password("normalpass"),
            current_user_type="NORMAL_USER",
            have_interest_membership=False,
            userSlug="normal-user"
        )

    def test_validate_user_success_admin(self):
        """
        Test that an admin user providing correct credentials is redirected to /admin.
        """
        response = self.client.get(
            reverse('validate_user'),
            data={'email': 'admin@example.com', 'password': 'adminpass'}
        )
        self.assertEqual(response.status_code, 302)
        # Expect the admin user to be redirected to '/admin'
        self.assertEqual(response['Location'], '/admin')

        # Verify that the session contains the user's slug.
        self.assertEqual(self.client.session.get('user_slug'), self.admin_user.userSlug)

    def test_validate_user_success_normal(self):
        """
        Test that a normal (or member) user providing correct credentials is redirected to /member.
        """
        response = self.client.get(
            reverse('validate_user'),
            data={'email': 'normal@example.com', 'password': 'normalpass'}
        )
        self.assertEqual(response.status_code, 302)
        # Expect a redirect to '/member'
        self.assertEqual(response['Location'], '/member')
        self.assertEqual(self.client.session.get('user_slug'), self.normal_user.userSlug)

    def test_validate_user_wrong_password(self):
        """
        Test that providing an incorrect password returns a JSON error with status 401.
        """
        response = self.client.get(
            reverse('validate_user'),
            data={'email': 'normal@example.com', 'password': 'wrongpass'}
        )
        self.assertEqual(response.status_code, 401)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['statusCode'], 401)
        self.assertIn('Wrong Password', content['message'])

    def test_validate_user_nonexistent(self):
        """
        Test that providing an email not present in the database returns a JSON error with status 404.
        """
        response = self.client.get(
            reverse('validate_user'),
            data={'email': 'nonexistent@example.com', 'password': 'nopass'}
        )
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['statusCode'], 404)
        self.assertIn('does not exist', content['message'])


class InsertUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user to test duplicate registration later.
        self.existing_email = "duplicate@example.com"
        Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Existing.User@togetherculture.com",
            first_name="Existing",
            last_name="User",
            email=self.existing_email,
            password=make_password("somepass"),
            current_user_type="NORMAL_USER",
            have_interest_membership=False,
            userSlug="existing-user"
        )

    def test_insert_user_success(self):
        """
        Test that a POST with valid registration data creates a new user,
        sets session user_slug, and redirects to getInitialInterests.
        """
        post_data = {
            'firstName': "John",
            'lastName': "Doe",
            'email': "john.doe@example.com",
            'password': "strongpassword",
            'terms': "on",  # This means haveInterestMembership will be True.
            'phone_number': "5551234567",
            'address': "123 Main St",
            'gender': "Male",
            'date_of_birth': "1990-01-01"
        }
        response = self.client.post(reverse('insert_user'), data=post_data)
        # Expect a redirect to the initial interests page (dummy returns 200)
        self.assertEqual(response.status_code, 302)
        # Redirect location should match what dummy_get_initial_interests returns. In this example,
        # the dummy function will normally return a redirect URL based on how Django processes the redirect.
        # You may examine response['Location'] if needed.
        # Check that a user was created.
        new_user = Users.objects.get(email="john.doe@example.com")
        self.assertEqual(new_user.first_name, "John")
        self.assertEqual(new_user.have_interest_membership, True)
        # Verify the session now contains the new user's slug.
        self.assertEqual(self.client.session.get('user_slug'), new_user.userSlug)

    def test_insert_user_duplicate(self):
        """
        Test that attempting to register using an email that already exists returns a JSON error.
        """
        post_data = {
            'firstName': "Jane",
            'lastName': "Smith",
            'email': self.existing_email,  # duplicate email
            'password': "anotherpass",
            'terms': "on",
            'phone_number': "5557654321",
            'address': "456 Elm St",
            'gender': "Female",
            'date_of_birth': "1985-05-05"
        }
        response = self.client.post(reverse('insert_user'), data=post_data)
        self.assertEqual(response.status_code, 500)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content['statusCode'], 500)
        self.assertIn('User registration failed', content['message'])
