import sys
import time
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import Examiner
from .models import Student
#from .models import Score
from .models import *
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
    #if not Score.objects.filter(student_id=id).exists():
        #result = Score.objects.create(student_id=id)
        #result.save()
        #return redirect('primary:testsPage')
    return redirect('primary:testsPage')

@login_required(login_url="/primary/login")
def rpdNamingObjTst(request):
    
    student_instance = Student.objects.get(id=request.session['student'])
    print(student_instance)
    global stime
    global etime
    global timeWrongAnswers
    global num
    global test_id

    if request.POST.get("formtype3"):        
        reason = request.POST["submitTst"]
        testResult = RpdNamingObj_Score.objects.create(student_id = student_instance, startT_A = stime, endT_A = etime, wrongAns_A = num, reason_A = reason)
        testResult.save()
        test_id = testResult.pk
        if reason == "تم الانتهاء من بنود الاختبار كلها ":
            return redirect("primary:rpdNamingObjTstB")
        else:
            return redirect(reverse('primary:testsPage'))

    if request.htmx:
        if request.POST.get("formtype1"):
            stime = datetime.now()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime = datetime.now()
            num = 0
            timeDiff = (etime - stime).total_seconds()
            selection = request.POST.getlist('selection','')  
            img = []
            img.extend(request.POST.getlist('selection',''))
            count = len(img)
            num = count
            if selection:
                timeWrongAnswers = timeDiff + count
                return HttpResponse(timeWrongAnswers)
            else:
                timeWrongAnswers = timeDiff + count
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingObjTst.html")
    
@login_required(login_url="/primary/login")
def rpdNamingObjTstB(request):
    global stime2
    global etime2
    global num2
    global timeWrongAnswers2

    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        RpdNamingObj_Score.objects.filter(id=test_id).update(startT_B = stime2, endT_B = etime2, wrongAns_B = num2, reason_B = reason)
        return redirect("primary:testsPage")
    
    if request.htmx:
        if request.POST.get("formtype1"):
            stime2 = datetime.now()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime2 = datetime.now()
            num2 = 0
            timeDiff2 = (etime2 - stime2).total_seconds()
            print(int(timeDiff2))
            selection2 = request.POST.getlist('selection','')  
            img2 = []
            img2.extend(request.POST.getlist('selection',''))
            count2 = len(img2)
            num2 = count2

            if selection2:
                timeWrongAnswers2 = timeDiff2 + count2
                return HttpResponse(timeWrongAnswers2)
            else:
                timeWrongAnswers2 = timeDiff2 + count2
                return HttpResponse('Test Ended')
    return render (request,"primary/rpdNamingObjTstB.html")

@login_required(login_url="/primary/login")
def rpdNamingLtrTst(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global stime3
    global etime3
    global num3
    global ltrTest_id
    global timeWrongAnswers3
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        testResult = RpdNamingLtrs_Score.objects.create(student_id = student_instance, startT_A = stime3, endT_A = etime3, wrongAns_A = num3, reason_A = reason)
        testResult.save()
        ltrTest_id = testResult.pk
        if reason == "تم الانتهاء من بنود الاختبار كلها ":
            return redirect("primary:rpdNamingLtrTstB")
        else:
            return redirect(reverse('primary:testsPage'))
        
    if request.htmx:
        if request.POST.get("formtype1"):
            stime3 = datetime.now()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime3 = datetime.now()
            num3 = 0
            timeDiff3 = (etime3 - stime3).total_seconds()
            selection3 = request.POST.getlist('selection','')  
            img3 = []
            img3.extend(request.POST.getlist('selection',''))
            count3 = len(img3)
            num3 = count3
            if selection3:
                timeWrongAnswers3 = timeDiff3 + count3
                return HttpResponse(timeWrongAnswers3)
            else:
                timeWrongAnswers3 = timeDiff3 + count3
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingLtrTst.html")

@login_required(login_url="/primary/login")
def rpdNamingLtrTstB(request):
    global stime4
    global etime4
    global num4
    global timeWrongAnswers4
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        RpdNamingLtrs_Score.objects.filter(id=ltrTest_id).update(startT_B = stime4, endT_B = etime4, wrongAns_B = num4, reason_B = reason)
        return redirect("primary:testsPage")
    if request.htmx:
        if request.POST.get("formtype1"):
            stime4 = datetime.now()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            etime4 = datetime.now()
            num4 = 0
            timeDiff4 = (etime4 - stime4).total_seconds()
            print(int(timeDiff4))
            selection4 = request.POST.getlist('selection','')  
            img4 = []
            img4.extend(request.POST.getlist('selection',''))
            count4 = len(img4)
            num4 = count4
            if selection4:
                timeWrongAnswers4 = timeDiff4 + count4
                return HttpResponse(timeWrongAnswers4)
            else:
                timeWrongAnswers4 = timeDiff4 + count4
                return HttpResponse('Test Ended')
    return render (request,"primary/rpdNamingLtrTstB.html")

@login_required(login_url="/primary/login")
def phonemSyllableTraining(request):
    return render(request, "primary/phonemSyllableTraining.html")

@login_required(login_url="/primary/login")
def phonemeSyllableDel(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global test_id
    global counter
    global endTime
    global selectionA

    if request.POST.get("form2"):
        reason = request.POST["submitTst"]
        testResult = PhonemeSyllableDel.objects.create(student_id = student_instance,  correctAns = counter, reason = reason , date=endTime)
        testResult.save()
        test_id = testResult.pk
        return redirect("primary:testsPage")
    if request.htmx:
        if request.POST.get("form1"):
            endTime = datetime.now()
            selectionA = request.POST.getlist('selection','')  
            answers = []
            answers.extend(request.POST.getlist('selection',''))
            counter = len(answers)
            print(counter)
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
    rpdnamingObj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
    rpdNamingLtrs = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
    phonemeSyllDel = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
    global context_obj
    context_obj = {} 
    global context_ltrs
    context_ltrs = {}
    global context_phoneme
    context_phoneme = {} 
    student = Student.objects.get(id=request.session['student']).studentName

    if (rpdnamingObj.exists() or rpdNamingLtrs.exists() or phonemeSyllDel.exists()):
        RpdNamingObj_Score_obj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
        RpdNamingLtrs_Score_obj = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
        phonemeDel_Score_obj = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
        if(RpdNamingObj_Score_obj.exists()):
            
            rpdNOwrongA_A = RpdNamingObj_Score.objects.filter(student_id = request.session['student']).latest("id")
            
            rpdNOwrongA = rpdNOwrongA_A.wrongAns_A
            
            rpdNOwrongB = RpdNamingObj_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            
            if ((rpdNOwrongA != None and rpdNOwrongB != None)):

                stimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                stimeB=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_B
                etimeB=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durationA=etimeA-stimeA
                durationA=round(durationA.total_seconds())
                durationB=etimeB-stimeB
                durationB = round(durationB.total_seconds())
                scoreA=rpdNOwrongA+durationA
                scoreB=rpdNOwrongB+durationB
                total=scoreA+scoreB
                context_obj = {"rpdNOwrongA":(rpdNOwrongA),  "rpdNOwrongB":(rpdNOwrongB), "durationA":(durationA),"durationB":(durationB) , "scoreA":(scoreA) , "scoreB":(scoreB), "totalScore_obj":(round(total)), "status_obj":('منجز '),}
            elif (rpdNOwrongA != None and rpdNOwrongB == None):
                stimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durationA=etimeA-stimeA
                durationA=round(durationA.total_seconds())
                scoreA=rpdNOwrongA+durationA
                total=scoreA
                
                context_obj = {"rpdNOwrongA":(rpdNOwrongA), "totalScore_obj":(round(total)), "status_obj":('توقف '),}
        else:
            context_obj = { "status_obj":('غير منجز'),}

        if(RpdNamingLtrs_Score_obj.exists()):
            
            rpdNLwrongA = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_A
            rpdNLwrongB = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            if ((rpdNLwrongA != None and rpdNLwrongB != None)):
                
                stimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                stimeLTRB=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_B
                etimeLTRB=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durationTstA=etimeLTRA-stimeLTRA
                durationTstA=round(durationTstA.total_seconds())
                durationTstB=etimeLTRB-stimeLTRB
                durationTstB = round(durationTstB.total_seconds())
                scoreTstA=rpdNLwrongA+durationTstA
                scoreTstB=rpdNLwrongB+durationTstB
                totalScore=scoreTstA+scoreTstB
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),  "rpdNLwrongB":(rpdNLwrongB),"durationTstA":(durationTstA),"durationTstB":(durationTstB) , "scoreTstA":(scoreTstA) , "scoreTstB":(scoreTstB), "totalScore_ltr":(round(totalScore)), "status_ltrs":('منجز '),  }
                
            elif (rpdNLwrongA != None and rpdNLwrongB == None):
                
                stimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durationTstA=etimeLTRA-stimeLTRA
                durationTstA=round(durationTstA.total_seconds())
                scoreTstA=rpdNLwrongA+durationTstA
                totalScore=scoreTstA
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),"totalScore_ltr":(round(totalScore)),"status_ltrs":('توقف '),}
        else:
            context_ltrs = { "status_ltrs":('غير منجز'),}

        if(phonemeDel_Score_obj.exists()):
            phonemeSyllDelAns = PhonemeSyllableDel.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (phonemeSyllDelAns != None):
                context_phoneme = {"correctAnswers":(phonemeSyllDelAns), "status_phoneme":('منجز '), }
            else:
                context_phoneme = {"status_phoneme":('غير منجز'), }
        else:
            context_phoneme = {"status_phoneme":('غير منجز'), }

        return render(request, "primary/testsPage.html", {"context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme":context_phoneme,"student": student,})
    else:
        context_obj = { "status_obj":('غير منجز'),}
        context_ltrs = { "status_ltrs":('غير منجز'),}
        return render(request,"primary/testsPage.html", {"context_obj": context_obj, "context_ltrs": context_ltrs,"student":(Student.objects.get(id=request.session['student']).studentName) })

    