from django.db import models

# Create your models here.

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'users'
    

class UserTypes(models.Model):
    userId = models.IntegerField()
    userType = models.CharField(max_length=100)
    date = models.DateTimeField()
    class Meta:
        db_table = 'user_types'