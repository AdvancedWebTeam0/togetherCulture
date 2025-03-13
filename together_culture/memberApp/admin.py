from django.contrib import admin
from .models import DigitalContentModule, ModuleBooking, Membership, MembershipType, Benefit

# Register your models here.

admin.site.register(DigitalContentModule)
admin.site.register(ModuleBooking)
admin.site.register(Membership)
admin.site.register(MembershipType)
admin.site.register(Benefit)
