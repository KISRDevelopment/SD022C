import sys
import time
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import Examiner
from .models import Student
from .models import Score
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
    print(id)
    print('start test')
    if not Score.objects.filter(student_id=id).exists():
        result = Score.objects.create(student_id=id)
        result.save()
        return redirect('primary:testsPage')
    return redirect('primary:testsPage')

@login_required(login_url="/primary/login")
def rpdNamingObjTst(request):
    result = Score.objects.get(student_id=request.session['student'])
    global stime
    global etime
    global timeWrongAnswers
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        result.rpdNOA_reason=reason
        result.save()
        return redirect("primary:rpdNamingObjTstB")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime = datetime.now()
            # stime = datetime.fromtimestamp(time.mktime(time.localtime()))
            result.rpdNOA_startT = stime
            result.save()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime = datetime.now()
            # etime = datetime.fromtimestamp(time.mktime(time.localtime()))
            result.rpdNOA_endT = etime
            timeDiff = (etime - stime).total_seconds()
            selection = request.POST.getlist('selection','')  
            img = []
            img.extend(request.POST.getlist('selection',''))
            count = len(img)
            result.rpdNOA_wrongAns=count
            result.save()
            if selection:
                # timeDiff = int(timeDiff.total_seconds())
                # print(timeDiff)
                timeWrongAnswers = timeDiff + count
                # result.timeWrngAnsA=timeWrongAnswers
                # result.save()
                return HttpResponse(timeWrongAnswers)
            else:
                # timeDiff = int(timeDiff.total_seconds())
                timeWrongAnswers = timeDiff + count
                # result.rpdNOA_wrongAns=count
                # result.save()
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingObjTst.html")
    
@login_required(login_url="/primary/login")
def rpdNamingObjTstB(request):
    result2 = Score.objects.get(student_id=request.session['student'])
    global stime2
    global etime2
    global timeWrongAnswers2
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        result2.rpdNOB_reason=reason
        result2.save()
        return redirect("primary:testsPage")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime2 = datetime.now()
            # stime2 = datetime.fromtimestamp(time.mktime(time.localtime()))
            result2.rpdNOB_startT = stime2
            result2.save()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime2 = datetime.now()
            # etime2 = datetime.fromtimestamp(time.mktime(time.localtime()))
            result2.rpdNOB_endT = etime2
            timeDiff2 = (etime2 - stime2).total_seconds()
            print(int(timeDiff2))
            selection2 = request.POST.getlist('selection','')  
            img2 = []
            img2.extend(request.POST.getlist('selection',''))
            count2 = len(img2)
            result2.rpdNOB_wrongAns = count2
            result2.save()
            if selection2:
                # timeDiff2 = int(timeDiff2.total_seconds())
                timeWrongAnswers2 = timeDiff2 + count2
                return HttpResponse(timeWrongAnswers2)
            else:
                # timeDiff2 = int(timeDiff2.total_seconds())
                timeWrongAnswers2 = timeDiff2 + count2
                return HttpResponse('Test Ended')
    return render (request,"primary/rpdNamingObjTstB.html")

@login_required(login_url="/primary/login")
def rpdNamingLtrTst(request):
    result3 = Score.objects.get(student_id=request.session['student'])
    global stime3
    global etime3
    global timeWrongAnswers3
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        result3.rpdNLA_reason=reason
        result3.save()
        return redirect("primary:rpdNamingLtrTstB")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime3 = datetime.now()
            # stime = datetime.fromtimestamp(time.mktime(time.localtime()))
            result3.rpdNLA_startT = stime3
            result3.save()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime3 = datetime.now()
            # etime = datetime.fromtimestamp(time.mktime(time.localtime()))
            result3.rpdNLA_endT = etime3
            timeDiff3 = (etime3 - stime3).total_seconds()
            selection3 = request.POST.getlist('selection','')  
            img3 = []
            img3.extend(request.POST.getlist('selection',''))
            count3 = len(img3)
            result3.rpdNLA_wrongAns=count3
            result3.save()
            if selection3:
                # timeDiff = int(timeDiff.total_seconds())
                # print(timeDiff)
                timeWrongAnswers3 = timeDiff3 + count3
                # result.timeWrngAnsA=timeWrongAnswers
                # result.save()
                return HttpResponse(timeWrongAnswers3)
            else:
                # timeDiff = int(timeDiff.total_seconds())
                timeWrongAnswers3 = timeDiff3 + count3
                # result.rpdNOA_wrongAns=count
                # result.save()
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingLtrTst.html")

@login_required(login_url="/primary/login")
def rpdNamingLtrTstB(request):
    result4 = Score.objects.get(student_id=request.session['student'])
    global stime4
    global etime4
    global timeWrongAnswers4
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        result4.rpdNLB_reason=reason
        result4.save()
        return redirect("primary:testsPage")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime4 = datetime.now()
            # stime2 = datetime.fromtimestamp(time.mktime(time.localtime()))
            result4.rpdNLB_startT = stime4
            result4.save()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime4 = datetime.now()
            # etime2 = datetime.fromtimestamp(time.mktime(time.localtime()))
            result4.rpdNLB_endT = etime4
            timeDiff4 = (etime4 - stime4).total_seconds()
            print(int(timeDiff4))
            selection4 = request.POST.getlist('selection','')  
            img4 = []
            img4.extend(request.POST.getlist('selection',''))
            count4 = len(img4)
            result4.rpdNLB_wrongAns = count4
            result4.save()
            if selection4:
                # timeDiff2 = int(timeDiff2.total_seconds())
                timeWrongAnswers4 = timeDiff4 + count4
                return HttpResponse(timeWrongAnswers4)
            else:
                # timeDiff2 = int(timeDiff2.total_seconds())
                timeWrongAnswers4 = timeDiff4 + count4
                return HttpResponse('Test Ended')
    return render (request,"primary/rpdNamingLtrTstB.html")

@login_required(login_url="/primary/login")
def phonemSyllableTraining(request):
    return render(request, "primary/phonemSyllableTraining.html")

@login_required(login_url="/primary/login")
def phonemeSyllableDel(request):
    if request.POST.get("formtypeB"):
        print('-------------------')
        return redirect("primary:testsPage")
    if request.htmx:
        print('htmx post')
        if request.POST.get("formtypeA"):
            print('+++++++++++++++')
            selectionA = request.POST.getlist('selection','')  
            answers = []
            answers.extend(request.POST.getlist('selection',''))
            counter = len(answers)
            if selectionA:
                print(counter)
                return HttpResponse('Test s')
            else:
                return HttpResponse('Test Ended')
    return render (request,"primary/phonemeSyllableDel.html")

@login_required(login_url="/primary/login")
def nonWordRepetitionTraining(request):
    return render(request, "primary/nonWordRepetitionTraining.html")

@login_required(login_url="/primary/login")
def nonWordRepetition(request):
    if request.POST.get("form2"):
        print('-------------------')
        return redirect("primary:testsPage")
    if request.htmx:
        print('htmx post')
        if request.POST.get("form1"):
            print('+++++++++++++++')
            selectionA = request.POST.getlist('selection','')  
            answers = []
            answers.extend(request.POST.getlist('selection',''))
            counter = len(answers)
            if selectionA:
                print(counter)
                return HttpResponse('Test s')
            else:
                return HttpResponse('Test Ended')
    return render (request,"primary/nonWordRepetition.html")

@login_required(login_url="/primary/login")
def nonWordReadingAccuracy(request):
    if request.method == "POST":
        return redirect('primary:nonWordReadingAccuracy')
    return render(request, "primary/nonWordReadingAccuracy.html")


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
    rpdNOwrongA = Score.objects.get(student_id=request.session['student']).rpdNOA_wrongAns
    rpdNOwrongB = Score.objects.get(student_id=request.session['student']).rpdNOB_wrongAns
    rpdNLwrongA = Score.objects.get(student_id=request.session['student']).rpdNLA_wrongAns
    rpdNLwrongB = Score.objects.get(student_id=request.session['student']).rpdNLB_wrongAns
    if (rpdNOwrongA != None and rpdNOwrongB != None): 
        stimeA=Score.objects.get(student_id=request.session['student']).rpdNOA_startT
        etimeA=Score.objects.get(student_id=request.session['student']).rpdNOA_endT
        stimeB=Score.objects.get(student_id=request.session['student']).rpdNOB_startT
        etimeB=Score.objects.get(student_id=request.session['student']).rpdNOB_endT
        durationA=etimeA-stimeA
        durationA=round(durationA.total_seconds())
        durationB=etimeB-stimeB
        durationB = round(durationB.total_seconds())
        scoreA=rpdNOwrongA+durationA
        scoreB=rpdNOwrongB+durationB
        total=scoreA+scoreB
        return render(request,"primary/testsPage.html", {
            "rpdNOwrongA":(rpdNOwrongA),  "rpdNOwrongB":(rpdNOwrongB),"durationA":(durationA),"durationB":(durationB) , "scoreA":(scoreA) , "scoreB":(scoreB), "totalScore":(round(total)), "status":('منجز ') , "student":(Score.objects.get(student_id=request.session['student']).student),      
        })
    if (rpdNLwrongA != None and rpdNLwrongB != None):
        print('not none') 
        strtimeA=Score.objects.get(student_id=request.session['student']).rpdNLA_startT
        endtimeA=Score.objects.get(student_id=request.session['student']).rpdNLA_endT
        strtimeB=Score.objects.get(student_id=request.session['student']).rpdNLB_startT
        endtimeB=Score.objects.get(student_id=request.session['student']).rpdNLB_endT
        durationTstA=endtimeA-strtimeA
        durationTstA=round(durationTstA.total_seconds())
        durationTstB=endtimeB-strtimeB
        durationTstB = round(durationTstB.total_seconds())
        scoreTstA=rpdNLwrongA+durationTstA
        scoreTstB=rpdNLwrongB+durationTstB
        totalScore=scoreTstA+scoreTstB
        return render(request,"primary/testsPage.html", {
            "rpdNLwrongA":(rpdNLwrongA),  "rpdNLwrongB":(rpdNLwrongB),"durationTstA":(durationTstA),"durationTstB":(durationTstB) , "scoreTstA":(scoreTstA) , "scoreTstB":(scoreTstB), "totalScore":(round(totalScore)), "status":('منجز ') , "student":(Score.objects.get(student_id=request.session['student']).student),      
        })
    else:
        return render(request,"primary/testsPage.html", {"status":('غير منجز ') ,"student":(Score.objects.get(student_id=request.session['student']).student) })
