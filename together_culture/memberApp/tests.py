from django.test import TestCase, Client
from django.urls import reverse
from loginRegistrationApp.models import Users,Events, UserAttendingEvent,UserInterests,UserTypes
from memberApp.models import DigitalContentModule, ModuleBooking, Benefit, Membership, MembershipType
from datetime import date
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
import uuid
from datetime import datetime, timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from django.contrib import messages

class DigitalContentModuleTestCase(TestCase):
    def setUp(self):
        """Set up test data for DigitalContentModule and ModuleBooking."""
        # Create a test user
        self.user = Users.objects.create(
            user_id="8d36c361-6392-46ff-a755-5f27ca33c773", user_name="testuser", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="Admin",
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
            email="john@example.com", password="password", current_user_type="Admin",
            userSlug = 'user'
        )

        self.user2 = Users.objects.create(
            user_id="d8ac4feb-e18a-4107-9df4-7aa093f38604", user_name="testuser1",
            first_name="John", last_name="Doe", email="memebr@example.com", password="password",
            current_user_type="member", userSlug = 'user2'
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
            start_date=date.today(),
            end_date=date.today(),
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
        self.assertEqual(str(self.membership), "TestUser - Premium (2025-03-25)")
        
class BenefitTest(TestCase):
    
    def setUp(self):
        """Setup test data."""
        self.user = Users.objects.create(user_name="TestUser")
        self.membership_type = MembershipType.objects.create(
            name='Premium', duration_days=30, price=29.99)
        
        self.membership = Membership.objects.create(
            user=self.user,
            membership_type=self.membership_type,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
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
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('member-dashboard')

    def test_member_dashboard_logged_in(self):
        """Test that the member dashboard view works for a logged-in user."""
        self.client.login(username='testuser', password='testpassword')  # Log in the user
        response = self.client.get(self.url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'member_dashboard.html')

        # Check if the context contains the correct title
        self.assertContains(response, 'Member Dashboard')

        # Check if the context contains the correct username
        self.assertContains(response, 'testuser')
        
class BenefitsViewTest(TestCase):

    def setUp(self):
        """Set up a user and necessary data for the test."""
        # Create the user
        self.user1 = Users.objects.create(
            user_id="17776ae2-4bc8-47d3-8169-ce46d86e9e7a", 
            user_name="testuser1", 
            first_name="John", 
            last_name="Doe", 
            email="john@example.com", 
            password="password", 
            current_user_type="Admin",
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
        self.assertIn('membership_types', response.context)
        self.assertGreater(len(response.context['membership_types']), 0)  # Ensure there are membership types
        
        # Check that the benefit is correctly passed in the context
        benefit = response.context['benefits'][0]
        self.assertEqual(benefit.name, "Free Content")
        self.assertEqual(benefit.remaining(), 5)  # The benefit should have 5 uses remaining

    def test_benefits_view_no_user(self):
        """Test that the benefits view redirects to login if the user is not logged in."""
        
        # Make a GET request to the 'benefits' view without being logged in
        response = self.client.get(self.url)
        
        # Check if it redirects to login
        self.assertRedirects(response, '/loginRegistration/login/?next=' + self.url)


# ======= Settings View Tests =======
class SettingsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user using your custom Users model.
        self.user = Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Test$User",  # initial user_name (will be re-generated in view)
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password=make_password("initialpass"),
            current_user_type="NORMAL_USER",
            have_interest_membership=False,
            userSlug="test-user",   # initial slug
            phone_number="1234567890",
            address="123 Test St",
            gender="Male"
        )
        # Simulate an authenticated session by setting user_slug.
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()

    def test_get_with_authenticated_user_renders_settings_page(self):
        """GET with a valid user_slug should render settings.html with status 200."""
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        self.assertEqual(response.context['user'].userSlug, self.user.userSlug)

    def test_get_without_valid_user_slug_redirects_to_login(self):
        """GET without user_slug (or with an invalid one) should redirect to login."""
        # Remove user_slug from session.
        session = self.client.session
        session.pop('user_slug', None)
        session.save()
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        # Set an invalid slug.
        session = self.client.session
        session['user_slug'] = "nonexistent-slug"
        session.save()
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_post_valid_data_updates_user_info_and_password(self):
        """POST with valid data should update user info, regenerate slug, update password, and redirect."""
        new_first_name = "Updated"
        new_last_name = "User"
        new_password = "newpass123"
        post_data = {
            'first_name': new_first_name,
            'last_name': new_last_name,
            'phone_number': "0987654321",
            'address': "321 Updated Ave",
            'gender': "Female",
            'new_password': new_password,
            'confirm_password': new_password,
        }
        response = self.client.post(reverse('settings'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('settings'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, new_first_name)
        self.assertEqual(self.user.last_name, new_last_name)
        self.assertEqual(self.user.user_name, f"{new_first_name}${new_last_name}")
        expected_slug = slugify(f"{new_first_name}${new_last_name}")
        self.assertIn(expected_slug, self.user.userSlug)
        self.assertNotEqual(self.user.password, new_password)
        self.assertTrue(check_password(new_password, self.user.password))
        session = self.client.session
        self.assertEqual(session.get('user_slug'), self.user.userSlug)

    def test_post_password_mismatch_shows_error(self):
        """POST with non-matching passwords should redirect to 'settings' without changing password."""
        old_password_hash = self.user.password
        post_data = {
            'new_password': "newpass123",
            'confirm_password': "differentpass",
        }
        response = self.client.post(reverse('settings'), post_data)
        # The view redirects on error.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('settings'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, old_password_hash)

# ======= Buy Membership View Tests =======
class BuyMembershipViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Member$User",
            first_name="Member",
            last_name="User",
            email="member@example.com",
            password=make_password("memberpass"),
            current_user_type="NORMAL_USER",
            have_interest_membership=False,
            userSlug="member-user",
            phone_number="1112223333",
            address="456 Member St",
            gender="Female"
        )
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        self.membership_type = MembershipType.objects.create(
            name="Premium",
            duration_days=30,
            price=9.99
        )
        self.invalid_membership_type = "NonExistent"

    def test_get_with_valid_session_renders_buy_membership_page(self):
        """GET with valid session should render buy_membership.html with current membership info."""
        response = self.client.get(reverse('buy_membership'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buy_membership.html')
        self.assertIn('current_membership', response.context)

    def test_get_without_session_redirects_to_login(self):
        """GET without user_slug should redirect to login."""
        session = self.client.session
        session.pop('user_slug', None)
        session.save()
        response = self.client.get(reverse('buy_membership'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/loginRegistration/login/')

    def test_post_missing_membership_type_returns_400(self):
        """POST without membership_type should return JSON with statusCode 400."""
        response = self.client.post(reverse('buy_membership'), data={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get('statusCode'), 400)
        self.assertIn('Membership type is required', data.get('message', ''))

    def test_post_invalid_membership_type_returns_404(self):
        """POST with an invalid membership_type should return JSON with statusCode 404."""
        response = self.client.post(reverse('buy_membership'), data={'membership_type': self.invalid_membership_type})
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get('statusCode'), 404)
        self.assertIn('Invalid membership type', data.get('message', ''))

    def test_post_valid_membership_creates_membership(self):
        """POST with valid membership_type should create a new Membership and update user's type."""
        response = self.client.post(reverse('buy_membership'), data={'membership_type': self.membership_type.name})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get('statusCode'), 200)
        self.assertIn('Membership purchased successfully', data.get('message', ''))
        self.assertTrue(Membership.objects.filter(user=self.user, active=True).exists())
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_user_type, "MEMBER")

# ======= Book Event View Tests =======
class BookEventViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Book$Er",
            first_name="Book",
            last_name="Er",
            email="booker@example.com",
            password=make_password("bookpass"),
            current_user_type="MEMBER",
            have_interest_membership=False,
            userSlug="book-er",
            phone_number="5555555555",
            address="789 Booker St",
            gender="Male"
        )
        self.event = Events.objects.create(
            eventId=100,
            eventName="Test Event",
            eventDate=datetime.now(),
            startTime=datetime.now().time(),
            endTime=(datetime.now() + timedelta(hours=2)).time(),
            location="Test Location",
            numberOfAttendees=0,
            shortDescription="Short Desc",
            longDescription="Long Description of Event",
            eventSlug="test-event",
            eventType="HA"
        )
        # For duplicate testing, no booking exists initially.
        # Note: warnings regarding naive datetime are expected if timezone support is active.

    def test_post_without_session_returns_401(self):
        """POST with valid JSON but without user_slug in session should return 401 Unauthorized."""
        # No user_slug set in session.
        payload = json.dumps({"eventId": self.event.eventId})
        response = self.client.post(reverse('book_event'),
                                    data=payload,
                                    content_type='application/json')
        # Expect 401 due to missing user_slug.
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content.decode())
        self.assertIn("User not logged in", data.get("message", ""))

    

    def test_post_valid_new_booking_creates_booking(self):
        """A valid POST with eventId should create a booking and return success JSON."""
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        # Ensure no previous booking exists.
        self.assertFalse(UserAttendingEvent.objects.filter(user=self.user, event=self.event).exists())
        payload = json.dumps({"eventId": self.event.eventId})
        response = self.client.post(reverse('book_event'),
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get("status"), "success")
        self.assertTrue(data.get("is_new_booking"))
        self.event.refresh_from_db()
        self.assertEqual(self.event.numberOfAttendees, 1)
        self.assertTrue(UserAttendingEvent.objects.filter(user=self.user, event=self.event).exists())

    def test_post_duplicate_booking_returns_already_booked(self):
        """If user already booked the event, the view should return an 'already_booked' status."""
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        # Create an initial booking.
        UserAttendingEvent.objects.create(user=self.user, event=self.event, isUserAttended=False)
        payload = json.dumps({"eventId": self.event.eventId})
        response = self.client.post(reverse('book_event'),
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get("status"), "already_booked")
        self.assertFalse(data.get("is_new_booking"))
        self.event.refresh_from_db()
        # Attendee count should remain unchanged (assuming duplicate booking does not increment it).
        self.assertEqual(self.event.numberOfAttendees, 0)

    def test_post_invalid_json_returns_400(self):
        """POST with malformed JSON should return 400 Bad Request."""
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        invalid_json = '{"eventId": '  # malformed JSON
        response = self.client.post(reverse('book_event'),
                                    data=invalid_json,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode())
        self.assertIn("Invalid JSON", data.get("message", ""))

    def setUp(self):
        self.client = Client()
        # Create a test user.
        self.user = Users.objects.create(
            user_id=uuid.uuid4(),
            user_name="Book$Er",
            first_name="Book",
            last_name="Er",
            email="booker@example.com",
            password=make_password("bookpass"),
            current_user_type="MEMBER",
            have_interest_membership=False,
            userSlug="book-er",
            phone_number="5555555555",
            address="789 Booker St",
            gender="Male"
        )
        # Create a test event. Ensure required fields are provided.
        self.event = Events.objects.create(
            eventId=100,
            eventName="Test Event",
            eventDate=datetime.now(),
            startTime=datetime.now().time(),
            endTime=(datetime.now() + timedelta(hours=2)).time(),
            location="Test Location",
            numberOfAttendees=0,
            shortDescription="Short Desc",
            longDescription="Long Description of Event",
            eventSlug="test-event",
            eventType="HA"  # assuming "HA" is one of the valid choices
        )
        # Do not log in by default here so that we can test unauthenticated behavior.


    def test_post_valid_new_booking_creates_booking(self):
        """POST with valid eventId should create a booking and increment event attendee count."""
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        # Ensure no previous booking exists
        self.assertFalse(UserAttendingEvent.objects.filter(user=self.user, event=self.event).exists())
        response = self.client.post(reverse('book_event'),
                                    data=json.dumps({"eventId": self.event.eventId}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get("status"), "success")
        self.assertTrue(data.get("is_new_booking"))
        # Verify the event attendee count increased.
        self.event.refresh_from_db()
        self.assertEqual(self.event.numberOfAttendees, 1)
        # Verify a booking record was created.
        self.assertTrue(UserAttendingEvent.objects.filter(user=self.user, event=self.event).exists())

    def test_post_duplicate_booking_returns_already_booked(self):
        """POST for an event the user already booked should indicate an already booked status."""
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        # Create an initial booking.
        UserAttendingEvent.objects.create(user=self.user, event=self.event, isUserAttended=False)
        response = self.client.post(reverse('book_event'),
                                    data=json.dumps({"eventId": self.event.eventId}),
                                    content_type="application/json")
        # Depending on your view logic, the duplicate booking might return status 200 with a special message.
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data.get("status"), "already_booked")
        self.assertFalse(data.get("is_new_booking"))
        # The attendee count should not have increased.
        self.event.refresh_from_db()
        self.assertEqual(self.event.numberOfAttendees, 0)

    def test_post_invalid_json_returns_400(self):
        """POST with invalid JSON should return 400 Bad Request."""
        session = self.client.session
        session['user_slug'] = self.user.userSlug
        session.save()
        invalid_json = '{"eventId": '  # malformed JSON
        response = self.client.post(reverse('book_event'),
                                    data=invalid_json,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content.decode())
        self.assertIn("Invalid JSON", data.get("message", ""))
