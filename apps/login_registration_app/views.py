# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import * 
from .forms import Registration_Form, Login_Form
import bcrypt

# Create your views here.
def index(request):
    #if there's a logged user, redirect to success page
    if 'logged_email' in request.session:
        return redirect(reverse('logreg:success'))
    registration_form = Registration_Form()
    login_form = Login_Form()
    return render(request, 'index.html', {'registration_form': registration_form, 'login_form': login_form})
def register(request):
    #do front end validation using form class
    form = Registration_Form(request.POST)
    if form.is_valid():
        #do back end valdations using model validator
        errors = User.objects.validate_user(form.cleaned_data)
        if len(errors) > 0:
            #log errors if model validator finds any
            for error in errors:
                messages.error(request, error)
                return redirect(reverse('logreg:index'))
        else:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            birthday = form.cleaned_data['birthday']
            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password, birthday=birthday)
            request.session['logged_email'] = email
            return redirect(reverse('logreg:success'))
    else:
        #log errors if form class finds any
        for key in form.errors:
            for item in form.errors[key]:
                string = key + ': ' + item
                messages.error(request, string)
        return redirect(reverse('logreg:index'))
def success(request):
    logged_user = User.objects.get(email=request.session['logged_email'])
    return render(request, 'success.html', {'user': logged_user})
def login(request):
    #validate form with form class
    form = Login_Form(request.POST)
    if form.is_valid():
        #grab user from database
        users = User.objects.filter(email = form.cleaned_data['email'])
        if len(users) < 1:
            #if no user found, throw error
            messages.error(request, 'No user with that email found')
            return redirect(reverse('logreg:index'))
        else:
            password = form.cleaned_data['password']
            #check if password entered matches password in database
            if bcrypt.checkpw(password.encode(), users[0].password.encode()):
                request.session['logged_email'] = form.cleaned_data['email']
                return redirect(reverse('logreg:success'))
            else:
                messages.error(request, 'That password does not match what is on file')
                return redirect(reverse('logreg:index'))
    else:
        #log form class errors
        for key in form.errors:
            for item in form.errors[key]:
                string = key + ': ' + item
                messages.error(request, string)
                return redirect(reverse('logreg:index'))
def logout(request):
    #clear session and redirect to index when logout is clicked
    request.session.clear()
    return redirect(reverse('logreg:index'))