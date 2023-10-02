import sys
import os
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import Examiner
from .models import Student
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Create your views here.
def index (request):
    return render (request,"primary/index.html")

def adminPage (request):
    return render (request,"primary/adminPage.html")

@login_required(login_url="/primary/login")
def signupSuperUser (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        speciality = request.POST['speciality']
        organization = request.POST['organization']
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken')
            return HttpResponseRedirect("signupSuperUser")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            examiner = Examiner.objects.create( name=name, speciality=speciality, organization=organization, user_id=user.id, admin_id=request.user.id)
            examiner.save()
            return HttpResponseRedirect("superusers")
        
    else:
        return render (request,"primary/signupSuperUser.html")
    
@login_required(login_url="/primary/login")
def signupStudents (request):
    if request.method == 'POST':
        studentName = request.POST['studentName']
        sex = request.POST['sex']
        schoolName = request.POST['schoolName']
        grade = request.POST['grade']
        eduDistrict = request.POST['eduDistrict']
        nationality = request.POST['nationality']
        examDate  = request.POST['examDate']
        birthDate = request.POST['birthDate']
        age = request.POST['age']

        if Student.objects.filter(studentName=studentName).exists():
            messages.info(request, 'student Name is already taken')
            return HttpResponseRedirect("signupStudents")
        else:
            student = Student.objects.create(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, eduDistrict=eduDistrict , nationality=nationality, examDate=examDate, birthDate=birthDate,age=age)
            student.save()
            return HttpResponseRedirect("students")
        
    else:
        return render (request,"primary/signupStudents.html")
    
def login (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.user.is_staff:
                return HttpResponseRedirect("superusers")
            else:
                return HttpResponseRedirect("examinerPage")
        else:
            messages.info(request, 'Invalid Username or Password')
            return HttpResponseRedirect("login")
    else:
        return render(request, "primary/login.html")

def help (request):
    return render (request,"primary/help.html")

def about (request):
    return render (request,"primary/about.html")
    
def contact (request):
    return render (request,"primary/contact.html")

def requestPage (request):
    return render (request,"primary/requestPage.html")

@login_required(login_url="/primary/login")
def superusers (request):
    if request.user.is_staff:
        return render(request,"primary/superusers.html", {
            "examiners": Examiner.objects.filter(admin_id=request.user.id)
        })
    else:
        return redirect(reverse('primary:examinerPage'))
      
def students (request):
    return render(request,"primary/students.html", {
        "students": Student.objects.all()
    })

@login_required(login_url="/primary/login")
def delete(request, id):
    userAccount = User.objects.filter(id=id)

    if request.method == "POST":
        userAccount.delete()

        return redirect(reverse('primary:superusers'))

    return render(request, 'primary/superusers.html')

@login_required(login_url="/primary/login")
def edit(request, id):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST['name']
        speciality = request.POST['speciality']
        organization = request.POST['organization']
        user = Examiner.objects.filter(user_id=id)
        userAccount = User.objects.filter(id=id)
        userDetails = User.objects.get(id=id)
        
        if password:
            userAccount.update(password = make_password(password))
        if User.objects.filter(username=username).exists() and username != userDetails.username:
                messages.info(request, 'Username is already taken')
        else:
            userAccount.update(username = username)

        user.update(name=name, speciality= speciality, organization=organization)

        return redirect(reverse('primary:superusers'))
    else:
        return render(request, 'primary/superusers.html')

def logout(request):
    auth.logout(request)
    return redirect(reverse('primary:index'))


def examinerPage (request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect(reverse('primary:superusers'))
        else:
            return render(request,"primary/examinerPage.html")
    
    return redirect(reverse('primary:index'))

def profile (request):
    if (request.user.is_staff):
        return render(request, 'primary/profile.html')
    else:
        return render(request, "primary/profile.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})
        
        

''' 
def password(request, id):
    if request.method == "POST":
        if(request.user.is_staff):
         password = request.POST["password"]
         user = user.objects.filter(id=id)
         if password: user.update(password = make_password(password)) 
         
        else:
         password = request.POST["password"]
         examiner = Examiner.objects.filter(id=id)
         if password: examiner.update(password = make_password(password)) 
              
        return redirect(reverse('primary:profile/'))
    else:
        return render(request, 'primary/profile.html', {
        "examiners": Examiner.objects.get(user_id=request.user.id)}) '''






