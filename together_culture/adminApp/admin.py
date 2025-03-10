from django.contrib import admin

# Register your models here.

from .models import EventTag, EventLabel

admin.site.register(EventTag)
admin.site.register(EventLabel)
