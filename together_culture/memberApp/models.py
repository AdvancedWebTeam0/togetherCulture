from django.db import models
from loginRegistrationApp.models import Users


class DigitalContentModule(models.Model):
    module_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'digital_content_modules'

    def __str__(self):
        return self.title


class ModuleBooking(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    module = models.ForeignKey(DigitalContentModule, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)
    date_booked = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'module_bookings'

    def __str__(self):
        return f"{self.user.user_name} booked {self.module.title}"
