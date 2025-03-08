from django.test import TestCase, Client
from django.urls import reverse
from loginRegistrationApp.models import Users
from memberApp.models import DigitalContentModule, ModuleBooking
from unittest.mock import patch
from django.contrib.auth.models import User


class DigitalContentModuleTestCase(TestCase):
    def setUp(self):
        """Set up test data for DigitalContentModule and ModuleBooking."""
        # Create a test user
        self.user = Users.objects.create(
            user_id="1", user_name="testuser", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="Admin"
        )

        # Create a digital content module
        self.module = DigitalContentModule.objects.create(
            title="Test Module",
            description="This is a test description.",
            duration=60
        )

    def test_digital_content_module_creation(self):
        """Test if a DigitalContentModule is created correctly."""
        module = DigitalContentModule.objects.get(title="Test Module")
        self.assertEqual(module.description, "This is a test description.")
        self.assertEqual(module.duration, 60)
        self.assertIsNotNone(module.date_created)

    def test_module_booking_creation(self):
        """Test if a ModuleBooking is created correctly."""
        booking = ModuleBooking.objects.create(
            user=self.user, module=self.module, is_booked=True)

        self.assertEqual(booking.user.user_name, "testuser")
        self.assertEqual(booking.module.title, "Test Module")
        self.assertTrue(booking.is_booked)
        self.assertIsNotNone(booking.date_booked)

    def test_str_methods(self):
        """Test the string representations of the models."""
        self.assertEqual(str(self.module), "Test Module")

        booking = ModuleBooking.objects.create(
            user=self.user, module=self.module, is_booked=True)
        self.assertEqual(str(booking), "testuser booked Test Module")


class DigitalContentViewTestCase(TestCase):
    def setUp(self):
        """Set up test data for the views."""
        self.client = Client()

        # Create a test user
        self.user = Users.objects.create(
            user_id="1", user_name="testuser1", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="Admin"
        )

        # Create a digital content module
        self.module = DigitalContentModule.objects.create(
            title="Test Module",
            description="This is a test description.",
            duration=60
        )

    def test_digital_content_view(self):
        """Test if digital_content view loads correctly and contains modules."""
        response = self.client.get(
            reverse('digital-content'))  # Update with the actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'digital_content.html')
        # Check if module title is in response
        self.assertContains(response, "Test Module")

    def test_book_module_success(self):
        """Test if a module can be booked successfully."""
        session = self.client.session
        # Manually set user ID in session
        session['_auth_user_id'] = self.user.pk
        session.save()

        response = self.client.post(
            reverse('book-module', args=[self.module.module_id]))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(
            data['message'], 'You have successfully booked the module!')

        # Ensure the booking was created
        self.assertTrue(ModuleBooking.objects.filter(
            user=self.user, module=self.module, is_booked=True).exists())

    def test_book_module_already_booked(self):
        """Test if a user cannot book the same module twice."""
        session = self.client.session
        # Manually set user ID in session
        session['_auth_user_id'] = self.user.pk
        session.save()
        
        # Create an initial booking
        ModuleBooking.objects.create(
            user=self.user, module=self.module, is_booked=True)

        # Try booking again
        response = self.client.post(
            reverse('book-module', args=[self.module.module_id]))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertEqual(
            data['message'], 'You have already booked this module.')

    def test_book_module_invalid_request(self):
        """Test if non-POST requests return an error."""
        session = self.client.session
        # Manually set user ID in session
        session['_auth_user_id'] = self.user.pk
        session.save()
        
        # Sending GET instead of POST
        response = self.client.get(
            reverse('book-module', args=[self.module.module_id]))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Invalid request.')
