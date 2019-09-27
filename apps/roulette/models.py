from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["first_name"]) <2:
            errors["first_name"]= "First Name should be at least 2 characters"

        if len(postData["last_name"]) <2:
            errors["last_name"]= "Last Name should be at least 2 characters"

        if len(postData["password"]) <8:
            errors["password"]= "Password is too short!!!"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")

        if postData["confirm_PW"] != postData["password"]:
            errors["password"]="Password does not match!!"

        user = User.objects.filter(email=postData['email'])
        if user:
            errors['already_registered'] = "Email is already registered. Please log in."

        return errors

    def login_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")

        if len(postData["password"]) <8:
            errors["password"]= "Password is too short!!!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username =  models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Restaurant(models.Model):
    image = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    user_saved = models.ManyToManyField (User, related_name ="saved")
    users = models.ManyToManyField (User, related_name ="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Note(models.Model):
    content = models.TextField(null=True)
    user = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant, related_name="restaurant_name", on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
