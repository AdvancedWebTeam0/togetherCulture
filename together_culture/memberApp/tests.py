from django.test import TestCase, Client
from django.urls import reverse
from loginRegistrationApp.models import Users
from memberApp.models import DigitalContentModule, ModuleBooking, Benefit, Membership, MembershipType
from datetime import date
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

class DigitalContentModuleTestCase(TestCase):
    def setUp(self):
        """Set up test data for DigitalContentModule and ModuleBooking."""
        # Create a test user
        self.user = Users.objects.create(
            user_id="8d36c361-6392-46ff-a755-5f27ca33c773", user_name="testuser", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="ADMIN",
            userSlug = 'user'
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
            email="john@example.com", password="password", current_user_type="ADMIN",
            userSlug = 'user'
        )

        self.user2 = Users.objects.create(
            user_id="d8ac4feb-e18a-4107-9df4-7aa093f38604", user_name="testuser1",
            first_name="John", last_name="Doe", email="memebr@example.com", password="password",
            current_user_type="MEMBER", userSlug = 'user2'
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

class MembershipTypeTest(TestCase):
    
    def setUp(self):
        """Setup test data."""
        self.membership_type = MembershipType.objects.create(
            name='Premium',
            duration_days=30,
            price=29.99
        )

    def test_membership_type_str(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.membership_type), 'Premium')
        
    def test_membership_type_fields(self):
        """Test if fields are set correctly."""
        self.assertEqual(self.membership_type.name, 'Premium')
        self.assertEqual(self.membership_type.duration_days, 30)
        self.assertEqual(self.membership_type.price, 29.99)

class MembershipTest(TestCase):
    
    def setUp(self):
        """Setup test data."""
        self.user = Users.objects.create(user_name="TestUser")
        self.membership_type = MembershipType.objects.create(
            name='Premium', duration_days=30, price=29.99)
        
        # Create a membership for the user
        self.membership = Membership.objects.create(
            user=self.user,
            membership_type=self.membership_type,
            start_date=timezone.datetime(2025, 3, 25),
            end_date=timezone.datetime(2025, 4, 20),
            active=True
        )

    def test_is_active_true(self):
        """Test the is_active() method returns True for active membership with a future end date."""
        self.membership.end_date = date.today() + timedelta(days=30)
        self.membership.save()
        self.assertTrue(self.membership.is_active())

    def test_is_active_false(self):
        """Test the is_active() method returns False for inactive membership or expired membership."""
        self.membership.active = False
        self.membership.save()
        self.assertFalse(self.membership.is_active())

        # Test expired membership
        self.membership.active = True
        self.membership.end_date = date.today() - timedelta(days=1)
        self.membership.save()
        self.assertFalse(self.membership.is_active())

    def test_membership_str(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.membership), "TestUser - Premium (2025-04-20 00:00:00)")
        
class BenefitTest(TestCase):
    
    def setUp(self):
        """Setup test data."""
        self.user = Users.objects.create(user_name="TestUser", password="testpassword")
        self.membership_type = MembershipType.objects.create(
            name='Premium', duration_days=30, price=29.99)
        
        self.membership = Membership.objects.create(
            user=self.user,
            membership_type=self.membership_type,
            start_date=timezone.datetime(2025, 3, 25),
            end_date=timezone.datetime(2025, 4, 20),
            active=True
        )

        self.benefit = Benefit.objects.create(
            name="Free Streaming",
            description="Access to free streaming for members",
            max_usage=5,
            used_count=0,
            membership=self.membership
        )
    
    def test_remaining_benefit(self):
        """Test the remaining method to calculate the remaining uses."""
        self.assertEqual(self.benefit.remaining(), 5)  # Max usage - used count
        
    def test_use_benefit_success(self):
        """Test using the benefit successfully."""
        result = self.benefit.use_benefit()
        self.assertTrue(result)  # Should return True if the benefit is used successfully
        self.benefit.refresh_from_db()
        self.assertEqual(self.benefit.used_count, 1)  # Used count should increase by 1
        
    def test_use_benefit_failure(self):
        """Test using the benefit beyond the max usage."""
        self.benefit.used_count = 5
        self.benefit.save()
        result = self.benefit.use_benefit()
        self.assertFalse(result)  # Should return False if the benefit cannot be used anymore
        self.benefit.refresh_from_db()
        self.assertEqual(self.benefit.used_count, 5)  # Used count should remain the same
        
    def test_benefit_str(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.benefit), 'Free Streaming')
        
class MemberDashboardTest(TestCase):

    def setUp(self):
        """Set up a user for testing."""
        self.user = Users.objects.create(
            user_id="14bf62e0-d4f1-487c-b71e-2e27726ef542", 
            user_name="testuser1", 
            first_name="John", 
            last_name="Doe", 
            email="john@example.com", 
            password="password", 
            current_user_type="ADMIN",
            userSlug="user1"
        )
        self.membership_type = MembershipType.objects.create(
            name='Premium', duration_days=30, price=29.99)
        
        self.membership = Membership.objects.create(
            user=self.user,
            membership_type=self.membership_type,
            start_date=timezone.datetime(2025, 3, 25),
            end_date=timezone.datetime(2025, 4, 20),
            active=True
        )

        self.benefit = Benefit.objects.create(
            name="Free Streaming",
            description="Access to free streaming for members",
            max_usage=5,
            used_count=0,
            membership=self.membership
        )
        self.url = reverse('member-dashboard')

    def test_member_dashboard_logged_in(self):
        """Test that the member dashboard view works for a logged-in user."""
        self.client.login(username='testuser1', password='password')
        response = self.client.get(self.url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'member_dashboard.html')

        # Check if the context contains the correct title
        self.assertContains(response, 'Member Dashboard')

        # Check if the context contains the correct username
        self.assertContains(response, 'testuser1')
        
class BenefitsViewTest(TestCase):

    def setUp(self):
        """Set up a user and necessary data for the test."""
        # Create the user
        self.user1 = Users.objects.create(
            user_id="14bf62e0-d4f1-487c-b71e-2e27726ef542", 
            user_name="testuser1", 
            first_name="John", 
            last_name="Doe", 
            email="john@example.com", 
            password="password", 
            current_user_type="ADMIN",
            userSlug="user1"
        )
        
        # Create a Membership Type (e.g., Premium)
        self.membership_type = MembershipType.objects.create(
            name="Premium",
            duration_days=30,
            price=19.99
        )
        
        # Create a Membership for the user
        self.membership = Membership.objects.create(
            user=self.user1,
            membership_type=self.membership_type,
            start_date=date.today(),
            end_date=date.today(),
            active=True
        )
        
        # Create Benefits for the user
        self.benefit = Benefit.objects.create(
            name="Free Content",
            description="Access to exclusive content.",
            max_usage=5,
            membership=self.membership
        )
        
        # URL for the benefits view
        self.url = reverse('benefits')

    def test_benefits_view(self):
        """Test that the benefits view works and passes correct context data."""
        
        # Simulate a request by logging in the test user
        self.client.login(username='testuser1', password='password')
        
        # Make a GET request to the 'benefits' view
        response = self.client.get(self.url)
        
        # Check the response status code (should be 200)
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct title is in the context
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Benefits')
        
        # Check that the user has the correct benefits in the context
        self.assertIn('benefits', response.context)
        self.assertEqual(len(response.context['benefits']), 1)  # One benefit associated with the user
        
        # Check that the membership types are in the context
        self.assertIn('membership_type', response.context)
        self.assertGreater(len(response.context['membership_type']), 0)  # Ensure there are membership types
        
        # Check that the benefit is correctly passed in the context
        benefit = response.context['benefits'][0]
        self.assertEqual(benefit.name, "Free Content")
        self.assertEqual(benefit.remaining(), 5)  # The benefit should have 5 uses remaining

    def test_benefits_view_no_user(self):
        """Test that the benefits view redirects to login if the user is not logged in."""
        
        # Make a GET request to the 'benefits' view without being logged in
        response = self.client.get(self.url)
        
        # Check if it redirects to login
        self.assertRedirects(response, '/loginRegistration/login/')