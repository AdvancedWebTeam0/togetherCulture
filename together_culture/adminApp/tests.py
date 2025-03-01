from loginRegistrationApp.models import Users, UserTypes
from loginRegistrationApp.models import Users
from django.test import TestCase, Client
import json
from django.http import JsonResponse
from loginRegistrationApp.models import Events, Users
from django.urls import reverse
from django.test import TestCase
from .models import EventTag, EventLabel
from django.db import IntegrityError
import json
from django.utils import timezone
from datetime import time
from django.contrib.auth.models import User


class EventTagModelTest(TestCase):
    def test_create_event_tag(self):
        # Create an EventTag object
        tag = EventTag.objects.create(eventTagName="Concert", required=False)
        # Check that the object is saved
        self.assertEqual(EventTag.objects.count(), 1)
        self.assertEqual(tag.eventTagName, "Concert")
        self.assertFalse(tag.required)

    def test_event_tag_unique(self):
        # Create the first EventTag
        EventTag.objects.create(eventTagName="Concert")
        # Try creating a duplicate EventTag, expecting IntegrityError due to the unique constraint
        with self.assertRaises(IntegrityError):
            EventTag.objects.create(eventTagName="Concert")

    def test_event_tag_str(self):
        tag = EventTag.objects.create(eventTagName="Music Festival")
        self.assertEqual(str(tag), "Music Festival")


class EventLabelModelTest(TestCase):
    def test_create_event_label(self):
        # Create an EventLabel object
        label = EventLabel.objects.create(eventLabelName="VIP", required=False)
        # Check that the object is saved
        self.assertEqual(EventLabel.objects.count(), 1)
        self.assertEqual(label.eventLabelName, "VIP")
        self.assertFalse(label.required)

    def test_event_label_unique(self):
        # Create the first EventLabel
        EventLabel.objects.create(eventLabelName="VIP")
        # Try creating a duplicate EventLabel, expecting IntegrityError due to the unique constraint
        with self.assertRaises(IntegrityError):
            EventLabel.objects.create(eventLabelName="VIP")

    def test_event_label_str(self):
        label = EventLabel.objects.create(eventLabelName="General Admission")
        self.assertEqual(str(label), "General Admission")


class ViewTests(TestCase):

    def test_admin_dashboard_view(self):
        # Test access to admin dashboard
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')
        self.assertIn('tags', response.context)
        self.assertIn('labels', response.context)
        self.assertIn('cards', response.context)

    def test_admin_dashboard_view_requires_login(self):
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_admin_dashboard_view_authenticated(self):
        user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('insights'))
        self.assertEqual(response.status_code, 200)


class InsightsViewTest(TestCase):

    def test_insights_view(self):
        response = self.client.get(reverse('insights'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insights.html')

    def test_insights_view_requires_login(self):
        response = self.client.get(reverse('insights'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_insights_view_authenticated(self):
        user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('insights'))
        self.assertEqual(response.status_code, 200)


class EventSearchViewTest(TestCase):

    def setUp(self):
        # Create test data for EventTag and EventLabel
        self.tag1 = EventTag.objects.create(eventTagName="Music")
        self.tag2 = EventTag.objects.create(eventTagName="Dance")
        self.label1 = EventLabel.objects.create(eventLabelName="VIP")
        self.label2 = EventLabel.objects.create(eventLabelName="General")

        # Set up the test client
        self.client = Client()

    def test_event_search_view_valid(self):

        # Create the event object with all required fields
        event = Events.objects.create(
            eventName="Test Eventsadfsdfa",
            eventDate=timezone.now(),  # current date and time
            startTime=time(10, 0),      # event start time: 10:00 AM
            endTime=time(12, 0),        # event end time: 12:00 PM
            location="Test Venue",
            numberOfAttenders=1,        # initial number of attendees
            shortDescription="A short description for testing.",
            longDescription="A longer, detailed description for the test event.",
            eventType=Events.EventType.HAPPENING,  # using the defined text choice
        )

        event.tags.add(self.tag1)
        event.labels.add(self.label1)

        tag_id = self.tag1.id
        label_id = self.label1.id

        # Test valid AJAX request for event search
        response = self.client.get(reverse(
            'event-search'), {'tags': str(tag_id), 'labels': str(label_id)}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('events', response_data)
        self.assertEqual(len(response_data['events']), 1)

    def test_event_search_view_no_results(self):

        tag_id = self.tag2.id
        label_id = self.label2.id

        # Test AJAX request with no matching events
        response = self.client.get(reverse(
            'event-search'), {'tags': str(tag_id), 'labels': str(label_id)}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)

        self.assertEqual(response_data['error'],
                         'No events found matching the criteria.')

    def test_event_search_view_invalid(self):
        # Test invalid AJAX request (wrong format)
        response = self.client.get(
            reverse('event-search'), {'tags': '1'}, HTTP_X_REQUESTED_WITH='NonAjax')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'],
                         'Invalid request, must be AJAX.')

    def test_event_search_no_filters(self):
        response = self.client.get(
            reverse('event-search'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # Ensure it returns no results
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'],
                         'No events found matching the criteria.')

    def test_event_search_view_non_existent_tag_label(self):
        response = self.client.get(reverse(
            # Non-existent IDs
            'event-search'), {'tags': '99999', 'labels': '99999'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'],
                         'No events found matching the criteria.')


class CreateTagLabelTest(TestCase):

    def test_save_tag_view_valid(self):
        # Test valid POST request to save a tag
        response = self.client.post(reverse('save-tag'),
                                    data=json.dumps({'tag_name': 'Festival'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(),
                             '{"success": true, "tag": "Festival"}')
        self.assertEqual(EventTag.objects.count(), 1)  # Ensure tag was created

    def test_save_tag_view_invalid(self):
        # Test POST with missing tag name
        response = self.client.post(reverse('save-tag'),
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(
        ), '{"success": false, "error": "No tag name provided"}')

    def test_save_label_view_valid(self):
        # Test valid POST request to save a label
        response = self.client.post(reverse('save-label'),
                                    data=json.dumps({'label_name': 'Premium'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(),
                             '{"success": true, "label": "Premium"}')
        # Ensure label was created
        self.assertEqual(EventLabel.objects.count(), 1)

    def test_save_label_view_invalid(self):
        # Test POST with missing label name
        response = self.client.post(reverse('save-label'),
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(
        ), '{"success": false, "error": "No label name provided"}')

    def test_save_tag_view_invalid_json(self):
        response = self.client.post(reverse('save-tag'),
                                    data="invalid-json-string",
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(
        ), '{"success": false, "error": "Invalid JSON data"}')


class UpdateCardViewTest(TestCase):

    def setUp(self):
        """
        This method will set up the test data, creating Users
        with `current_user_type='member'` and other necessary data.
        """
        # Create users with 'member' as current_user_type
        Users.objects.bulk_create(
            [Users(user_name=f'User{i}', first_name=f'First{i}', last_name=f'Last{i}',
                   email=f'user{i}@example.com', password='password', current_user_type='member') for i in range(130)]
        )
        # Create a few users with non-'member' user_type (e.g., 'admin')
        Users.objects.bulk_create(
            [Users(user_name=f'Admin{i}', first_name=f'AdminFirst{i}', last_name=f'AdminLast{i}',
                   email=f'admin{i}@example.com', password='password', current_user_type='admin') for i in range(5)]
        )

    def test_update_card_view_valid(self):
        """
        Test case for the valid card_id (1: Total number of members)
        which should return 130 members.
        """
        # Test valid card_id (card 1 for Total number of members)
        response = self.client.get(reverse('update-card', args=[1]))

        # Ensure the response is successful and returns the correct new_value
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), '{"new_value": 130}')

    def test_update_card_view_no_members(self):
        """
        Test case when there are no members in the Users table.
        """
        # Remove all users and re-run the test
        Users.objects.all().delete()

        # Test valid card_id (card 1 for Total number of members) with no members
        response = self.client.get(reverse('update-card', args=[1]))

        # Ensure the response is successful and returns the correct new_value
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), '{"new_value": 0}')

    def test_update_card_view_invalid_card_id(self):
        """
        Test case for an invalid card_id (should return a 400 error).
        """
        # Test with an invalid card_id (e.g., card_id=999 which doesn't exist)
        response = self.client.get(reverse('update-card', args=[999]))

        # Ensure the response status is 400 for an invalid card_id
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(),
                             '{"error": "Invalid card ID"}')

    def test_update_card_view_with_date_filter(self):
        """
        Test case for filtering based on a specific date for upcoming events.
        """
        # Create an event that is in the future
        future_event = Events.objects.create(
            eventName="Future event",
            startTime=time(10, 0),      # event start time: 10:00 AM
            endTime=time(12, 0),        # event end time: 12:00 PM
            location="Test Venue",
            numberOfAttenders=1,        # initial number of attendees
            shortDescription="A short description for testing.",
            longDescription="A longer, detailed description for the test event.",
            eventType=Events.EventType.HAPPENING,  # using the defined text choice
            eventDate=timezone.now() + timezone.timedelta(days=1)  # Tomorrow's date
        )

        # Create an event that is in the past
        past_event = Events.objects.create(
            eventName="Past event",
            startTime=time(10, 0),      # event start time: 10:00 AM
            endTime=time(12, 0),        # event end time: 12:00 PM
            location="Test Venue",
            numberOfAttenders=1,        # initial number of attendees
            shortDescription="A short description for testing.",
            longDescription="A longer, detailed description for the test event.",
            eventType=Events.EventType.HAPPENING,  # using the defined text choice
            eventDate=timezone.now() - timezone.timedelta(days=1)  # Yesterday's date
        )

        # Test card 2 (Number of upcoming events)
        response = self.client.get(reverse('update-card', args=[2]))

        # Ensure the response is successful and returns 1 upcoming event (the future event)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), '{"new_value": 1}')

    def test_update_card_view_invalid(self):
        # Test invalid card_id
        response = self.client.get(reverse('update-card', args=['invalid']))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content.decode(),
                             '{"error": "Invalid card ID"}')
