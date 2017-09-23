# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validate_user(self, data):
        errors = []
        name_regex = re.compile(r'^[A-Za-z]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        existing_email = User.objects.filter(email=data['email'])
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            errors.append('First name and last name must both be at least 2 characters')
        if not name_regex.match(data['first_name']) or not name_regex.match(data['last_name']):
            errors.append('Both first and last name must be letters only!')
        if len(data['email']) < 1:
            errors.append('Email is required')
        if not email_regex.match(data['email']):
            errors.append('Email is improperly formatted')
        if len(existing_email) > 0:
            errors.append('A user with that email already exist')
        if len(data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if data['password'] != data['confirm_password']:
            errors.append('Password and password confirmation must match')
        if data['birthday'].month != 1 and data['birthday'].month != 3 and data['birthday'].month != 5 and data['birthday'].month != 7 and data['birthday'].month != 8 and data['birthday'].month != 10 and data['birthday'].month != 12:
            if data['birthday'].month == 2:
                if data['birthday'].year % 4 != 0:
                    if data['birthday'].day > 28:
                        errors.append('Invalid day')
                elif data['birthday'].year % 100 == 0 and data['birthday'].year % 400 != 0:
                    if data['birthday'].day > 28:
                        errors.append('Invalid Day')
                else:
                    if data['birthday'].day > 29:
                        errors.append('Invalid Day')
            else:
                if data['birthday'].day > 30:
                    errors.append('Invalid Day')
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()