from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
            print("THiS1")
        if len(postData['last_name']) < 2:
            errors["last_name"] = "The last name should be at least 2 characters"
            print("THiS12")
        if len(postData['email']) < 5:
            errors["email"] = "The email should be at least 3 characters"
            print("THiS123")
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "The email should actually look like an email"
            print("problem5")
        if not (postData['first_name']).isalpha():
            errors['first_name'] = "First name should only contain letters"
            print("sucks for you")
            print(postData['first_name'])
        if not (postData['last_name']).isalpha():
            errors['last_name'] = "Last name should only contain letters"
            print("sucks for you too")
            print(postData['last_name'])
        if len(postData['password']) < 8:
            errors["release_date"] = "The password should be at least 8 characters"
            print("THiS1234")
        if postData['password'] != postData['c_password']:
            errors['password'] = "The passwords must match"
            print("THiS12345")
        users_matching = User.objects.filter(email = postData['email'])
        if len(users_matching) > 0:
            errors['email'] = "This email has been taken"
            print("Email exists already")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=255)
    objects = ShowManager() 

class Event(models.Model):
    title = models.CharField(max_length=255)
    when = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name="authors", on_delete=models.PROTECT)
    capacity = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="events")
    eventcode= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    formed =models.BooleanField(default = False)
    
class Team(models.Model):
    summary = models.TextField(max_length=1024)
    players = models.ManyToManyField(User, related_name='teams')
    eventcode= models.CharField(max_length=255)
