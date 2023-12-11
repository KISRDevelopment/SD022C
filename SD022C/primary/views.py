import sys
import time
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import Examiner
from .models import Student
from .models import rpdNamingObj
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from dateutil import relativedelta

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
        stage = request.POST['stage']
        name = request.POST['name']
        speciality = request.POST['speciality']
        organization = request.POST['organization']
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken')
            return HttpResponseRedirect("signupSuperUser")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            examiner = Examiner.objects.create( name=name, speciality=speciality, organization=organization, stage=stage, user_id=user.id, admin_id=request.user.id)
            examiner.save()
            return HttpResponseRedirect("superusers")
        
    else:
        return render (request,"primary/signupSuperUser.html")
    
@login_required(login_url="/primary/login")
def signupStudents (request):
    if request.method == 'POST':
        studentName = request.POST['studentName']
        sex = request.POST['gender']
        schoolName = request.POST['schoolName']
        grade = request.POST['grade']
        civilID = request.POST ['civilID']
        eduDistrict = request.POST['eduDistrict']
        nationality = request.POST['nationality']
        examDate  = request.POST['examDate']
        birthDate = request.POST['birthDate']

        examdate = datetime.strptime(request.POST['examDate'], '%Y-%m-%d')
        birthdate = datetime.strptime(request.POST['birthDate'], '%Y-%m-%d')

        delta = relativedelta.relativedelta(examdate, birthdate)
        print(delta.years, 'Years,', delta.months, 'months,', delta.days, 'days')
        age = str(delta.years) + "/" + str(delta.months) +"/"+str(delta.days)

        if Student.objects.filter(civilID=civilID).exists():
            messages.info(request, 'لقد تم تسجيل الطالب مسبقاً')
            return redirect("primary:signupStudents")
        else:
            student = Student.objects.create(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, civilID=civilID, eduDistrict=eduDistrict , nationality=nationality, examDate=examDate, birthDate=birthDate,age=age, examiner_id=request.user.id)
            student.save()
            return redirect("primary:students")
        
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
                return HttpResponseRedirect("students")

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
    request.session['student'] = 0
    return render(request,"primary/students.html", {
        "students": Student.objects.filter(examiner_id=request.user.id),  "stage": (Examiner.objects.get(user_id=request.user.id).stage)
    })

@login_required(login_url="/primary/login")
def delete(request, id):
    userAccount = User.objects.filter(id=id)

    if request.method == "POST":
        userAccount.delete()

        return redirect(reverse('primary:superusers'))

    return render(request, 'primary/superusers.html')

@login_required(login_url="/primary/login")
def deleteStudent(request,id):
    studentAccount = Student.objects.filter(id=id)

    if request.method == "POST":
        studentAccount.delete()
        return redirect(reverse('primary:students'))

    return render(request, "primary/students.html")

@login_required(login_url="/primary/login")
def startTest(request,id):
    request.session['student'] = id
    if request.method == "POST":
        if not rpdNamingObj.objects.filter(student_id=id).exists():
            result = rpdNamingObj.objects.create(student_id=id)
            result.save()
        return redirect('primary:testsPage')
    return render(request, "primary/students.html")

@login_required(login_url="/primary/login")
def rpdNamingObjTst(request):
    result = rpdNamingObj.objects.get(student_id=request.session['student'])
    global stime
    global etime
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        result.reasonA=reason
        result.save()
        return redirect("primary:rpdNamingObjTstB")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime = datetime.fromtimestamp(time.mktime(time.localtime()))
            result.start_timeA = time.strftime("%H:%M:%S")
            result.save()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            result.end_timeA = time.strftime("%H:%M:%S")
            result.statusA = 'Done'
            etime = datetime.fromtimestamp(time.mktime(time.localtime()))
            timeDiff = etime - stime
            result.durationA=timeDiff
            result.save()
            selection = request.POST.getlist('selection','')  
            img = []
            img.extend(request.POST.getlist('selection',''))
            count = len(img)
            if selection:
                timeDiff = int(timeDiff.total_seconds())
                timeWrongAnswers = timeDiff + count
                result.timeWrngAnsA=timeWrongAnswers
                result.save()
                return HttpResponse(timeDiff+count)
            else:
                timeDiff = int(timeDiff.total_seconds())
                timeWrongAnswers = timeDiff + count
                result.timeWrngAnsA=timeWrongAnswers
                result.save()
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingObjTst.html")
    
@login_required(login_url="/primary/login")
def rpdNamingObjTstB(request):
    result2 = rpdNamingObj.objects.get(student_id=request.session['student'])
    global stime
    global etime
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        result2.reasonB=reason
        result2.save()
        return redirect("primary:testsPage")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime = datetime.fromtimestamp(time.mktime(time.localtime()))
            result2.start_timeB = time.strftime("%H:%M:%S")
            result2.save()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            result2.end_timeB = time.strftime("%H:%M:%S")
            result2.statusB = 'Done'
            etime = datetime.fromtimestamp(time.mktime(time.localtime()))
            timeDiff2 = etime - stime
            result2.durationB=timeDiff2
            result2.save()
            selection2 = request.POST.getlist('selection','')  
            img2 = []
            img2.extend(request.POST.getlist('selection',''))
            count2 = len(img2)
            if selection2:
                timeDiff2 = int(timeDiff2.total_seconds())
                timeWrongAnswers2 = timeDiff2 + count2
                result2.timeWrngAnsB=timeWrongAnswers2
                result2.save()
                return HttpResponse(timeDiff2+count2)
            else:
                timeDiff2 = int(timeDiff2.total_seconds())
                timeWrongAnswers2 = timeDiff2 + count2
                result2.timeWrngAnsB=timeWrongAnswers2
                result2.save()
                return HttpResponse('Test Ended')
    return render (request,"primary/rpdNamingObjTstB.html")

@login_required(login_url="/primary/login")
def rpdNamingLtrTst(request):
    if request.method == "POST":
        return redirect('primary:rpdNamingLtrTst')
    return render(request, "primary/rpdNamingLtrTst.html")
@login_required(login_url="/primary/login")

def nonWrdAccuracyTst(request):
    if request.method == "POST":
        return redirect('primary:nonWrdAccuracyTst')
    return render(request, "primary/nonWrdAccuracyTst.html")


@login_required(login_url="/primary/login")
def editStudent(request, id):
    if request.method == "POST":
        studentName = request.POST['studentName']
        sex = request.POST['gender']
        schoolName = request.POST['schoolName']
        grade = request.POST['grade']
        eduDistrict = request.POST['eduDistrict']
        nationality = request.POST['nationality']
        
        birthDate_str = request.POST['birthDate']

        user = Student.objects.filter(id=id)
        userAccount = Student.objects.filter(examiner_id=id)

        user.update(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, eduDistrict=eduDistrict , nationality=nationality, birthDate=birthDate_str)

        return redirect(reverse('primary:students'))
    else:
        return render(request, 'primary/students.html' )
    
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

#show student details
def studentProfile(request, id):
        return render(request, "primary/studentProfile.html", {
        "students": Student.objects.filter(id=id)})

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
        
def testsPage (request):
    print('test page')
    result = rpdNamingObj.objects.get(student_id=request.session['student'])
    if request.method=="POST":
        print('form post')
        if result.statusA is not None and result.statusB is not None:
            print('test status: DONE')
            messages.info(request, 'لقد أجريت هذا الاختبار سابقا ')
            return render(request,"primary/testsPage.html")
        elif result.statusA is None:
            print('inside else')
            return render(request,"primary/testsPage.html")
    return render(request,"primary/testsPage.html")

