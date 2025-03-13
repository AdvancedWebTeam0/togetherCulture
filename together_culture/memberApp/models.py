from django.db import models
from loginRegistrationApp.models import Users
from datetime import date

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

# Membership Types (Plans)
class MembershipType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Free, Premium, VIP
    duration_days = models.PositiveIntegerField()  # How long the membership lasts
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Optional pricing

    def __str__(self):
        return self.name

# User Memberships
class Membership(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Many users can share the same plan
    membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def is_active(self):
        return self.active and self.end_date >= date.today()

    def __str__(self):
        return f"{self.user.user_name} - {self.membership_type.name} ({self.end_date})"


# Define a Benefit Model
class Benefit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    max_usage = models.PositiveIntegerField()  # Max times a user can use this benefit
    used_count = models.PositiveIntegerField(default=0)  # How many times the user has used it
    membership = models.ForeignKey(Membership, related_name="benefits", on_delete=models.CASCADE)
    
    def remaining(self):
        return self.max_usage - self.used_count
    
    def use_benefit(self):
        if self.used_count < self.max_usage:
            self.used_count += 1
            self.save()
            return True
        return False

    def __str__(self):
        return self.name