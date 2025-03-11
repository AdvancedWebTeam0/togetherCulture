from django.db import models

# Create your models here.


class EventTag(models.Model):
    eventTagName = models.CharField(max_length=100, unique=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.eventTagName

    class Meta:
        db_table = 'event_tag'


class EventLabel(models.Model):
    eventLabelName = models.CharField(max_length=100, unique=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.eventLabelName

    class Meta:
        db_table = 'event_label'
