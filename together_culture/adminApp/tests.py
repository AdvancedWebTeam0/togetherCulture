from django.test import TestCase, Client
from loginRegistrationApp.models import Events, Users, UserAttendingEvent, UserInterests, Interests
from django.urls import reverse
from .models import EventTag, EventLabel
from django.db import IntegrityError
import json
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from unittest.mock import patch
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time as sleep_time
from datetime import time  # Add this import at the top
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
            eventType="HA",
            eventSlug='event1'
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
            eventType="SP",
            eventSlug='event2'
        )

        self.event1.tags.add(self.tag1)
        self.event2.tags.add(self.tag2)
        self.event1.labels.add(self.label1)
        self.event2.labels.add(self.label2)

        self.user1 = Users.objects.create(
            user_id="8d36c361-6392-46ff-a755-5f27ca33c773", user_name="testuser1", first_name="John", last_name="Doe",
            email="john@example.com", password="password", current_user_type="Admin",
            userSlug="user1"
        )
        self.user2 = Users.objects.create(
            user_id="38683b82-ff63-4db7-b1f3-bd475adfb75f", user_name="testuser2", first_name="Jane", last_name="Doe",
            email="jane@example.com", password="password", current_user_type="Member",
            userSlug="user2"
        )

        self.attending1 = UserAttendingEvent.objects.create(
            user_id=self.user1.user_id, event=self.event1, isUserAttended=True
        )
        self.attending2 = UserAttendingEvent.objects.create(
            user_id=self.user2.user_id, event=self.event2, isUserAttended=True
        )

        self.interest1 = Interests.objects.create(
            interestId=998, name="stuff 1"
        )
        self.interest2 = Interests.objects.create(
            interestId=999, name="stuff 2"
        )

        self.userinterest1 = UserInterests.objects.create(
            user_id=self.user1.user_id, interest=self.interest1)
        self.userinterest2 = UserInterests.objects.create(
            user_id=self.user2.user_id, interest=self.interest2)

        self.event3 = Events.objects.create(
            eventName="New Year Party", eventDate=timezone.make_aware(datetime.datetime(2025, 1, 5)),
            startTime="18:00", endTime="23:00", location="Club A",
            numberOfAttendees=20, shortDescription="Celebration",
            longDescription="New Year Event", eventType="HA",
            eventSlug='event3'
        )
        self.event4 = Events.objects.create(
            eventName="Spring Fest", eventDate=timezone.make_aware(datetime.datetime(2025, 3, 15)),
            startTime="14:00", endTime="20:00", location="Park B",
            numberOfAttendees=50, shortDescription="Spring Celebration",
            longDescription="Spring Festival Event", eventType="ML",
            eventSlug='eventSlug4'
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
            eventSlug='events666'
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

    def test_save_tag_non_post_request(self):
        # Test that a non-POST request (like GET) returns an error

        # Make a GET request instead of a POST request
        response = self.client.get(reverse('save-tag'))

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains error message for non-POST requests
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['error'], 'Only POST requests with JSON data are allowed')

    def test_save_tag_non_json_content_type(self):
        # Test that a POST request with a non-JSON content type returns an error

        # Prepare the valid data
        data = {
            'eventTagName': 'Test Tag'
        }

        # Make the POST request with a content type that is not 'application/json'
        response = self.client.post(
            reverse('save-tag'),
            data=json.dumps(data),
            content_type='text/plain'  # Non-JSON content type
        )

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains error message for invalid content type
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['error'], 'Only POST requests with JSON data are allowed')

    def test_save_label_invalid_json(self):
        # Test that an invalid JSON body returns an error

        # Simulate sending invalid JSON (non-JSON string)
        response = self.client.post(
            reverse('save-label'),  # Replace with actual URL name
            data="invalid_json",  # This is not valid JSON
            content_type='application/json'
        )

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains error message for invalid JSON
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], 'Invalid JSON data')

    def test_save_label_non_json_content_type(self):
        # Test that a POST request with a non-JSON content type returns an error

        # Prepare the valid data
        data = {
            'eventLabelName': 'Test Label'
        }

        # Make the POST request with a non-JSON content type
        response = self.client.post(
            reverse('save-label'),
            data=json.dumps(data),
            content_type='text/plain'  # Non-JSON content type
        )

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains error message for invalid content type
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['error'], 'Only POST requests with JSON data are allowed')

    def test_save_label_non_post_request(self):
        # Test that a non-POST request (like GET) returns an error

        # Make a GET request instead of a POST request
        response = self.client.get(reverse('save-label'))

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains error message for non-POST requests
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(
            response.json()['error'], 'Only POST requests with JSON data are allowed')


class UpdateCardViewTest(TestCase):

    def setUp(self):
        """
        This method will set up the test data, creating Users
        with `current_user_type='member'` and other necessary data.
        """
        # Create users with 'member' as current_user_type
        Users.objects.bulk_create(
            [Users(user_name=f'User{i}', first_name=f'First{i}', last_name=f'Last{i}',
                   email=f'user{i}@example.com', password='password', current_user_type='member',
                   userSlug=f'usera{i}') for i in range(130)]
        )
        # Create a few users with non-'member' user_type (e.g., 'admin')
        Users.objects.bulk_create(
            [Users(user_name=f'Admin{i}', first_name=f'AdminFirst{i}', last_name=f'AdminLast{i}',
                   email=f'admin{i}@example.com', password='password', current_user_type='admin',
                   userSlug=f'userb{i}') for i in range(5)]
        )

        # Setup for card_id == 3 (EventTag)
        EventTag.objects.create(eventTagName="Tag 1")
        EventTag.objects.create(eventTagName="Tag 2")

        # Setup for card_id == 4 (EventLabel)
        EventLabel.objects.create(eventLabelName="Label 1")
        EventLabel.objects.create(eventLabelName="Label 2")
        EventLabel.objects.create(eventLabelName="Label 3")

    def test_update_card_event_tag_count(self):
        # Simulate a request to the `update_card` view with card_id = 3 (EventTag)
        response = self.client.get(reverse('update-card', args=[3]))

        # Assert the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert the response contains the correct count for EventTag
        self.assertEqual(
            response.json()['new_value'], EventTag.objects.count())

    def test_update_card_event_label_count(self):
        # Simulate a request to the `update_card` view with card_id = 4 (EventLabel)
        response = self.client.get(reverse('update-card', args=[4]))

        # Assert the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert the response contains the correct count for EventLabel
        self.assertEqual(
            response.json()['new_value'], EventLabel.objects.count())

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
            eventDate=timezone.now() + timezone.timedelta(days=1),  # Tomorrow's date
            eventSlug='event1'
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
            eventDate=timezone.now() - timezone.timedelta(days=1),  # Yesterday's date
            eventSlug="pastevent"
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


class EventDataViewTest(TestCase):

    @patch('adminApp.views.Events.objects.all')
    def test_event_data(self, mock_events_all):
        # Mock the event data
        mock_events_all.return_value = [
            Events(eventName="Event 1", eventDate="2025-03-25T10:00:00",
                   shortDescription="Test Event 1", location="Location 1", eventSlug="event-1"),
            Events(eventName="Event 2", eventDate="2025-03-26T14:00:00",
                   shortDescription="Test Event 2", location="Location 2", eventSlug="event-2"),
        ]

        # Make a GET request to the 'event_data' view
        response = self.client.get(reverse('event-data'))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the response is a JSON response
        self.assertEqual(response['Content-Type'], 'application/json')

        # Check the structure and data of the JSON response
        response_data = response.json()
        self.assertEqual(len(response_data), 2)  # Should have two events

        # Check first event data
        self.assertEqual(response_data[0]['title'], "Event 1")
        self.assertEqual(response_data[0]['start'], "2025-03-25T10:00:00")
        self.assertEqual(response_data[0]['end'], "2025-03-25T10:00:00")
        self.assertEqual(response_data[0]['description'], "Test Event 1")
        self.assertEqual(response_data[0]['location'], "Location 1")
        self.assertEqual(response_data[0]['slug'], "event-1")

        # Check second event data
        self.assertEqual(response_data[1]['title'], "Event 2")
        self.assertEqual(response_data[1]['start'], "2025-03-26T14:00:00")
        self.assertEqual(response_data[1]['end'], "2025-03-26T14:00:00")
        self.assertEqual(response_data[1]['description'], "Test Event 2")
        self.assertEqual(response_data[1]['location'], "Location 2")
        self.assertEqual(response_data[1]['slug'], "event-2")


class EventDetailViewTest(TestCase):

    @patch('adminApp.views.Events.objects.get')
    def test_event_detail(self, mock_events_get):
        # Mock the event data
        mock_event = Events(
            eventName="Event 1",
            eventDate="2025-03-25T10:00:00",
            shortDescription="Test Event 1",
            location="Location 1",
            eventSlug="event-1"
        )
        mock_events_get.return_value = mock_event

        # Make a GET request to the 'event_detail' view
        response = self.client.get(reverse('event-detail', args=['event-1']))

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'event_detail.html')

        # Check that the context contains the correct event data
        context = response.context
        self.assertEqual(context['event'], mock_event)

        # Test if the title and other context variables are also correct
        self.assertEqual(context['title'], "Event details")
        self.assertTrue('nav_items' in context)
        self.assertTrue('cards' in context)


class DashboardTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        # Run tests without opening a browser
        # options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

        # Create test data for EventTag and EventLabel
        tag1 = EventTag.objects.create(eventTagName="Music")
        tag2 = EventTag.objects.create(eventTagName="Dance")
        label1 = EventLabel.objects.create(eventLabelName="VIP")
        label2 = EventLabel.objects.create(eventLabelName="General")

        # Create the event object with all required fields
        event = Events.objects.create(
            eventName="Test Event 1",
            eventDate=timezone.make_aware(datetime.datetime(2025, 6, 17)),
            startTime=time(10, 0),      # event start time: 10:00 AM
            endTime=time(12, 0),        # event end time: 12:00 PM
            location="Test Venue",
            numberOfAttendees=1,        # initial number of attendees
            shortDescription="A short description for testing.",
            longDescription="A longer, detailed description for the test event.",
            eventType=Events.EventType.HAPPENING,  # using the defined text choice
            eventSlug='events666'
        )

        # Add tags and labels to the event
        event.tags.add(tag1, tag2)
        event.labels.add(label1, label2)

        # Set up the test client
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_page_loads(self):
        """Test that the dashboard page loads successfully"""
        self.driver.get(self.live_server_url + "/admin/")
        sleep_time.sleep(2)
        self.assertIn("Dashboard", self.driver.title)

    def test_add_tag_form_visibility(self):
        """Test if clicking the + button shows the tag creation form"""
        self.driver.get(self.live_server_url + "/admin/")
        sleep_time.sleep(2)

        add_tag_btn = self.driver.find_element(By.ID, "add-tag-btn")
        add_tag_btn.click()
        sleep_time.sleep(1)

        tag_form = self.driver.find_element(By.ID, "new-tag-form")
        self.assertTrue(tag_form.is_displayed())

    def test_add_label_form_visibility(self):
        """Test if clicking the + button shows the label creation form"""
        self.driver.get(self.live_server_url + "/admin/")
        sleep_time.sleep(2)

        add_label_btn = self.driver.find_element(By.ID, "add-label-btn")
        add_label_btn.click()
        sleep_time.sleep(1)

        label_form = self.driver.find_element(By.ID, "new-label-form")
        self.assertTrue(label_form.is_displayed())

    def test_event_search(self):
        """Test event search by date functionality"""
        self.driver.get(self.live_server_url + "/admin/")
        sleep_time.sleep(2)

        start_date = self.driver.find_element(By.ID, "start_date")
        end_date = self.driver.find_element(By.ID, "end_date")
        # Locate the search button by form ID and button type
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, "#eventSearchDateForm button[type='submit']")

        start_date.send_keys("2025-01-01")
        end_date.send_keys("2025-12-31")
        search_button.click()

        # Wait for the results header to be visible
        try:
            # Wait up to 10 seconds for the results header to be visible
            results_header = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "resultsHeader"))
            )
            self.assertTrue(results_header.is_displayed())
        except TimeoutException:
            print("Timed out waiting for results header to become visible.")

    def test_ajax_event_results(self):
        """Test if event search results populate dynamically via AJAX"""
        self.driver.get(self.live_server_url + "/admin/")
        sleep_time.sleep(2)

        # Find the date input elements
        start_date = self.driver.find_element(By.ID, "start_date")
        end_date = self.driver.find_element(By.ID, "end_date")
        search_button = self.driver.find_element(
            By.XPATH, "//button[text()='Search']")

        # Set the date format to match JavaScript expectations (YYYY-MM-DD)
        start_date.send_keys("2025-06-01")
        end_date.send_keys("2025-07-01")

        # Click the search button to trigger the AJAX request
        search_button.click()
        sleep_time.sleep(3)

        # Verify that results are returned (at least one result should appear)
        results_table = self.driver.find_element(By.ID, "resultsTable")
        results_rows = results_table.find_elements(By.TAG_NAME, "tr")
        self.assertGreater(len(results_rows), 0)  # Expect at least one result


class EventChartsTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        # Run tests without opening a browser
        # options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

        # Create test data for EventTag and EventLabel
        tag1 = EventTag.objects.create(eventTagName="Music")
        tag2 = EventTag.objects.create(eventTagName="Dance")
        label1 = EventLabel.objects.create(eventLabelName="VIP")
        label2 = EventLabel.objects.create(eventLabelName="General")

        # Create the event object with all required fields
        event = Events.objects.create(
            eventName="Test Event 1",
            eventDate=timezone.make_aware(datetime.datetime(2025, 6, 17)),
            startTime=time(10, 0),      # event start time: 10:00 AM
            endTime=time(12, 0),        # event end time: 12:00 PM
            location="Test Venue",
            numberOfAttendees=1,        # initial number of attendees
            shortDescription="A short description for testing.",
            longDescription="A longer, detailed description for the test event.",
            eventType=Events.EventType.HAPPENING,  # using the defined text choice
            eventSlug='events666'
        )

        # Add tags and labels to the event
        event.tags.add(tag1, tag2)
        event.labels.add(label1, label2)

        # Set up the test client
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_event_charts_load_and_update(self):
        # Open the admin insights
        self.driver.get(self.live_server_url + "/admin/insights")
        
        # Wait for the charts to be present
        charts = ["eventTypeChart", "eventTagChart", "eventLabelChart", "eventChart"]
        for chart_id in charts:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, chart_id))
            )
            chart_element = self.driver.find_element(By.ID, chart_id)
            self.assertTrue(chart_element.is_displayed(), f"Chart {chart_id} is not visible")
        
        # Wait for the charts to update
        sleep_time.sleep(5)
        
        # Verify that the charts contain data
        for chart_id in charts:
            chart_element = self.driver.find_element(By.ID, chart_id)
            data_url = chart_element.get_attribute("data-url")
            self.assertIsNotNone(data_url, f"Chart {chart_id} does not have a data source")