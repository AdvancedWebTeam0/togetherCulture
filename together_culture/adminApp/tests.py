from django.test import TestCase, Client
from loginRegistrationApp.models import Events, Users, UserAttendingEvent, UserInterests, Interests
from django.urls import reverse
from .models import EventTag, EventLabel
from django.db import IntegrityError
import json
from django.utils import timezone
from datetime import time
from django.contrib.auth.models import User
import datetime


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
    def setUp(self):
        self.tag1 = EventTag.objects.create(
            eventTagName="Music", required=True)
        self.tag2 = EventTag.objects.create(eventTagName="Sports")

        self.label1 = EventLabel.objects.create(
            eventLabelName="Outdoor", required=False)
        self.label2 = EventLabel.objects.create(eventLabelName="Online")

        self.event1 = Events.objects.create(
            eventName="Concert",
            eventDate=timezone.make_aware(datetime.datetime(2025, 5, 17)),
            startTime="18:00",
            endTime="22:00",
            location="Stadium",
            numberOfAttendees=100,
            shortDescription="A live concert",
            longDescription="A great live music experience",
            eventType="HA"
        )
        self.event2 = Events.objects.create(
            eventName="Football Match",
            eventDate=timezone.make_aware(datetime.datetime(2025, 4, 15)),
            startTime="15:00",
            endTime="17:00",
            location="Sports Arena",
            numberOfAttendees=200,
            shortDescription="A local match",
            longDescription="A thrilling football match",
            eventType="SP"
        )

        self.event1.tags.add(self.tag1)
        self.event2.tags.add(self.tag2)
        self.event1.labels.add(self.label1)
        self.event2.labels.add(self.label2)

        self.user1 = Users.objects.create(
            user_id="1", user_name="testuser1", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="Admin"
        )
        self.user2 = Users.objects.create(
            user_id="2", user_name="testuser2", first_name="Jane", last_name="Doe",
            email="jane@example.com", password="password", current_user_type="Member"
        )

        self.attending1 = UserAttendingEvent.objects.create(
            user_id=self.user1.user_id, event=self.event1, isUserAttended=True
        )
        self.attending2 = UserAttendingEvent.objects.create(
            user_id=self.user2.user_id, event=self.event2, isUserAttended=True
        )
        
        self.interest1 = Interests.objects.create(
            interestId = 998, name = "stuff 1"
        )
        self.interest2 = Interests.objects.create(
            interestId = 999, name = "stuff 2"
        )

        self.userinterest1 = UserInterests.objects.create(
            user_id=self.user1.user_id, interest=self.interest1)
        self.userinterest2 = UserInterests.objects.create(
            user_id=self.user2.user_id, interest=self.interest2)

        self.event3 = Events.objects.create(
            eventName="New Year Party", eventDate=timezone.make_aware(datetime.datetime(2025, 1, 5)),
            startTime="18:00", endTime="23:00", location="Club A",
            numberOfAttendees=20, shortDescription="Celebration",
            longDescription="New Year Event", eventType="HA"
        )
        self.event4 = Events.objects.create(
            eventName="Spring Fest", eventDate=timezone.make_aware(datetime.datetime(2025, 3, 15)),
            startTime="14:00", endTime="20:00", location="Park B",
            numberOfAttendees=50, shortDescription="Spring Celebration",
            longDescription="Spring Festival Event", eventType="ML"
        )

        self.attending1 = UserAttendingEvent.objects.create(
            user_id=self.user1.user_id, event=self.event3, isUserAttended=True
        )
        self.attending2 = UserAttendingEvent.objects.create(
            user_id=self.user2.user_id, event=self.event4, isUserAttended=True
        )

    def test_insights_view(self):
        # Ensure the correct URL name
        response = self.client.get(reverse('insights'))
        # Check if the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Verify that the correct counts are passed to the context
        self.assertEqual(response.context['num_users'], 2)
        self.assertEqual(response.context['num_events'], 4)
        self.assertEqual(response.context['num_attending_events'], 4)
        self.assertEqual(response.context['num_user_interests'], 2)

        # Check if the title is correctly passed
        self.assertEqual(response.context['title'], "Admin Insights")

    def test_insights_view_requires_login(self):
        response = self.client.get(reverse('insights'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_insights_view_authenticated(self):
        user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('insights'))
        self.assertEqual(response.status_code, 200)

    def test_event_type_data(self):
        response = self.client.get(reverse('event-type-data'))
        # Ensure API returns 200 OK
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('eventTypes', data)
        self.assertIn('eventTypeValues', data)

        # Verify event types match created events
        self.assertEqual(len(data['eventTypes']), 3)
        self.assertEqual(len(data['eventTypeValues']), 3)

    def test_event_tag_data(self):
        response = self.client.get(reverse('event-tag-data'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('eventTags', data)
        self.assertIn('eventTagValues', data)

        # Verify tags are counted correctly
        self.assertEqual(len(data['eventTags']), 2)
        self.assertEqual(len(data['eventTagValues']), 2)

    def test_event_label_data(self):
        response = self.client.get(reverse('event-label-data'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('eventLabels', data)
        self.assertIn('eventLabelValues', data)

        # Verify labels are counted correctly
        self.assertEqual(len(data['eventLabels']), 2)
        self.assertEqual(len(data['eventLabelValues']), 2)

    def test_events_per_month(self):
        response = self.client.get(reverse('events-per-month'))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('months', data)
        self.assertIn('event_counts', data)

        # Check if January and March have events
        self.assertEqual(data['event_counts'][0], 1)  # January
        self.assertEqual(data['event_counts'][2], 1)  # March

    def test_event_search_date(self):
        url = reverse('event-search-date')
        params = {
            'start_date': '2025-01-01',
            'end_date': '2025-01-31'
        }

        response = self.client.get(
            url, params, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('events', data)

        self.assertEqual(len(data['events']), 1)
        self.assertEqual(data['events'][0]['eventName'], "New Year Party")
        self.assertEqual(data['events'][0]['totalAttendees'], 1)

        # Check attendee details
        self.assertEqual(data['events'][0]['attendees'][0]['name'], "John Doe")
        self.assertEqual(data['events'][0]['attendees']
                         [0]['email'], "john@example.com")


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
            numberOfAttendees=1,        # initial number of attendees
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
            numberOfAttendees=1,        # initial number of attendees
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
            numberOfAttendees=1,        # initial number of attendees
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
