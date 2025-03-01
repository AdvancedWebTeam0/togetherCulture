from django.db import models
import uuid
from adminApp.models import EventTag, EventLabel

# Create your models here.


class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)  # Set user_id as primary key
    user_name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)  # Ensure email is unique
    password = models.CharField(max_length=255)  # Ensure enough length for hashed password
    current_user_type = models.CharField(max_length=45)
    have_interest_membership = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    

class UserTypes(models.Model):
    userId = models.IntegerField()
    userType = models.CharField(max_length=100)
    date = models.DateTimeField()
    class Meta:
        db_table = 'user_types'
    

class Events(models.Model):
    eventId = models.AutoField(primary_key=True)
    eventName = models.CharField(max_length=100)
    eventDate = models.DateTimeField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    location = models.CharField(max_length=100)
    numberOfAttenders = models.IntegerField(auto_created=0)
    shortDescription = models.CharField(max_length=50)
    longDescription = models.CharField(max_length=500)
    tags = models.ManyToManyField(EventTag, blank=True, related_name="events")
    labels = models.ManyToManyField(EventLabel, blank=True, related_name="events")

    class EventType(models.TextChoices):
        HAPPENING = "HA", "Happening"
        MEMBER_LED = "ML", "Member Led"
        CARING = "CA", "Caring"
        SHARING = "SH", "Sharing"
        LEARNING = "LE", "Learning"
        WORKING = "WO", "Working"
        DEMOCRACY = "DE", "Democracy"

    eventType = models.CharField(
        max_length=2,
        choices=EventType.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'


class UserAttendingEvent(models.Model):
    userId = models.IntegerField()
    eventId = models.IntegerField()
    isUserAttended = models.BooleanField(default=False)
    class Meta:
        db_table = 'user_attending_event'


class Interests(models.Model):
    interestId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'interests'


class UserInterests(models.Model):
    userId = models.IntegerField()
    interestId = models.IntegerField()
    class Meta:
        db_table = 'user_interests'
