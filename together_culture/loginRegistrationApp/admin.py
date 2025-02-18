from django.contrib import admin

# Register your models here.

from .models import Users, UserTypes, Events, UserAttendingEvent, Interests, UserInterests

admin.site.register(Users)
admin.site.register(UserTypes)
admin.site.register(Events)
admin.site.register(UserAttendingEvent)
admin.site.register(Interests)
admin.site.register(UserInterests)