from django.test import TestCase, Client
from django.urls import reverse
from loginRegistrationApp.models import Users
from memberApp.models import DigitalContentModule, ModuleBooking, Benefit, Membership, MembershipType
from datetime import date


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

        self.membership_type = MembershipType.objects.create(
            name="premium", duration_days=5, price=0)

        # Create a test user
        self.user = Users.objects.create(
            user_id="d8ac4feb-e18a-4107-9df4-7aa093f38603", user_name="testuser1", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="Admin"
        )

        self.user2 = Users.objects.create(
            user_id="d8ac4feb-e18a-4107-9df4-7aa093f38604", user_name="testuser1",
            first_name="John", last_name="Doe", email="memebr@example.com", password="password",
            current_user_type="member"
        )

        self.membership = Membership.objects.create(user=self.user2,
                                                    membership_type=self.membership_type, end_date=date(2025, 3, 22))

        self.benefit = Benefit.objects.create(name="book-modules",
                                              description="benefit to book modules",
                                              max_usage="5", used_count=5, membership=self.membership)

        # Create a digital content module
        for i in range(12):
            DigitalContentModule.objects.create(
                title=f"Module {i + 1}",
                description="This is a test description.",
                duration=60
            )

    def test_digital_content_view(self):
        """Test if digital_content view loads correctly and contains modules."""
        response = self.client.get(
            reverse('digital-content'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'digital_content.html')
