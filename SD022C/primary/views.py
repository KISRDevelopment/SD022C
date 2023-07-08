import sys
import os
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import Superusers

# Create your views here.
def index (request):
    return render (request,"primary/index.html")

def adminPage (request):
    return render (request,"primary/adminPage.html")

def signupSuperUser (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        speciality = request.POST['speciality']
        organization = request.POST['organization']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return HttpResponseRedirect("signupSuperUser")
            else:
                user = Superusers.objects.create(username=username, password=password, confirm_password=confirm_password, name=name, speciality=speciality, organization=organization)
                user.save()
                return HttpResponseRedirect("superusers")
        else:
            messages.info(request, 'Both passwords are not matching')
            return HttpResponseRedirect("signupSuperUser")
    else:
        return render (request,"primary/signupSuperUser.html")

def help (request):
    return render (request,"primary/help.html")

def login (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("adminPage")
        else:
            messages.info(request, 'Invalid Username or Password')
            return HttpResponseRedirect("login")
    else:
        return render(request, "primary/login.html")

def about (request):
    return render (request,"primary/about.html")
    
def contact (request):
    return render (request,"primary/contact.html")

def requestPage (request):
    return render (request,"primary/requestPage.html")

def superusers (request):
    return render (request,"primary/superusers.html")

