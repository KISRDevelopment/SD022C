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
import pandas as pd
from primary.utils import return_scores

# Create your views here.
global context_obj
context_obj = {} 
global context_ltrs
context_ltrs = {}
global context_phoneme
context_phoneme = {}
global context_nonWrdRep
context_nonWrdRep = {} 
global context_nonWrdReading
context_nonWrdReading = {} 
global score_phonemeDel
score_phonemeDel = {}
global score_obj
score_obj = {} 
global score_nonWrdRep
score_nonWrdRep = {}
global score_nonWrdReadingAcc
score_nonWrdReadingAcc = {} 

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
        
        #calculate age
        examdate = datetime.strptime(request.POST['examDate'], '%Y-%m-%d')
        birthdate = datetime.strptime(request.POST['birthDate'], '%Y-%m-%d')

        #CCET Manual Method
        e_Day = examdate.day
        e_Month = examdate.month
        e_Year = examdate.year
        b_Day = birthdate.day
        b_Month = birthdate.month
        b_Year = birthdate.year

        if ((e_Day - b_Day) < 0):
            e_Day = e_Day + 30
            e_Month = e_Month - 1
        days = e_Day - b_Day
        if ((e_Month - b_Month) < 0):
            e_Month = e_Month + 12
            e_Year = e_Year - 1
        months = e_Month - b_Month
        years = e_Year - b_Year

        #Method 1
        #delta = relativedelta.relativedelta(examdate, birthdate)
        #years = delta.years
        #months = delta.months
        #days = delta.days

        #Method 2
        #delta = examdate-birthdate  #total age in days = delat.days
        #years = math.floor(delta.days/365)    #calculate years
        #months = math.floor(((delta.days/365)%1)*12)  #calculate months
        #days = math.floor(((((delta.days/365)%1)*12)%1)*30)   #calculate days

        age = str(years) + "/" + str(months) +"/"+str(days)

        if Student.objects.filter(civilID=civilID).exists():
            messages.info(request, 'لقد تم تسجيل الطالب مسبقاً')
            return redirect("primary:signupStudents")
        else:
            student = Student.objects.create(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, civilID=civilID, eduDistrict=eduDistrict , nationality=nationality, examDate=examDate, birthDate=birthDate,age=age, examiner_id=request.user.id)
            student.save()
            return redirect("primary:students")
        
    else:
        return render (request,"primary/signupStudents.html", {
           "stage": (Examiner.objects.get(user_id=request.user.id).stage)
    })
    
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
        "students": Student.objects.filter(examiner_id=request.user.id),  "stage": (Examiner.objects.get(user_id=request.user.id).stage), "examiners": (Examiner.objects.get(user_id=request.user.id))
    })

def search_results(request):
    print("inside search_results")
    query = request.GET.get('search', '')
    print(f'"query = {query }"')

    all_students = Student.objects.filter(examiner_id=request.user.id)
    if query:
        students = all_students.filter(civilID__icontains=query)
        print(f'"Student at query {students}')
    else:
        students = []
        print(f'"Students at else {students}"')
    context={'students': students}
    return render(request, 'primary/students.html', context)

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
def editStudent(request, id):
    if request.method == "POST":
        studentName = request.POST['studentName']
        sex = request.POST['gender']
        schoolName = request.POST['schoolName']
        grade = request.POST['grade']
        eduDistrict = request.POST['eduDistrict']
        nationality = request.POST['nationality']
        examDate_str = request.POST['examDate']
        birthDate_str = request.POST['birthDate']

        user = Student.objects.filter(id=id)
        userAccount = Student.objects.filter(examiner_id=id)

        #Update Age
        examdate = datetime.strptime(request.POST['examDate'], '%Y-%m-%d')
        birthdate = datetime.strptime(request.POST['birthDate'], '%Y-%m-%d')

        e_Day = examdate.day
        e_Month = examdate.month
        e_Year = examdate.year
        b_Day = birthdate.day
        b_Month = birthdate.month
        b_Year = birthdate.year

        if ((e_Day - b_Day) < 0):
            e_Day = e_Day + 30
            e_Month = e_Month - 1
        days = e_Day - b_Day
        if ((e_Month - b_Month) < 0):
            e_Month = e_Month + 12
            e_Year = e_Year - 1
        months = e_Month - b_Month
        years = e_Year - b_Year

        age = str(years) + "/" + str(months) +"/"+str(days)
        print ("Age: ",age)

        user.update(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, eduDistrict=eduDistrict , nationality=nationality, birthDate=birthDate_str, examDate=examDate_str,age=age)

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

@login_required(login_url="/primary/login")
def startTest(request,id):
    request.session['student'] = id
    stage = (Examiner.objects.get(user_id=request.user.id).stage)
    print(stage)
    if stage == 'PRIMARY':
        return redirect('primary:testsPage')
    elif stage == 'SECONDARY':
        return redirect('primary:testsPageSec')
    else:
        return redirect('primary:testsPage')

# test 1 - A
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
    return render(request, "primary/rpdNamingObjTst.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 1 - B    
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
    return render (request,"primary/rpdNamingObjTstB.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 3 - A
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
    return render(request, "primary/rpdNamingLtrTst.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 3 - B
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
    return render (request,"primary/rpdNamingLtrTstB.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 2
@login_required(login_url="/primary/login")
def phonemSyllableTraining(request):
    return render(request, "primary/phonemSyllableTraining.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 2
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
    return render (request,"primary/phonemeSyllableDel.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 4
@login_required(login_url="/primary/login")
def nonWordRepetitionTraining(request):
    return render(request, "primary/nonWordRepetitionTraining.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 4
@login_required(login_url="/primary/login")
def nonWordRepetition(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global test_id
    global count
    global date
    global select
    if request.POST.get("form2"):
        reasonDropDown = request.POST["submitTst"]
        testResult = NonWordRepetition.objects.create(student_id = student_instance,  correctAns = count, reason = reasonDropDown , date=date)
        testResult.save()
        test_id = testResult.pk
        return redirect("primary:testsPage")
    if request.htmx:
        print('htmx post')
        if request.POST.get("form1"):
            date = datetime.now()
            select = request.POST.getlist('selection','')  
            choices = []
            choices.extend(request.POST.getlist('selection',''))
            count = len(choices)
            if select:
                print(count)
                return HttpResponse('Test s')
            else:
                return HttpResponse('Test Ended')
    return render (request,"primary/nonWordRepetition.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# test 5
@login_required(login_url="/primary/login")
def nonWordReadingAccuracy(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global test_id
    global count
    global dateTime

    if request.POST.get("dropDownForm"):
        reasonDropDown = request.POST["submitTst"]
        testResult = NonWordReadingAcc.objects.create(student_id = student_instance,  correctAns = count, reason = reasonDropDown , date=dateTime)
        testResult.save()
        test_id = testResult.pk
        return redirect("primary:testsPage")
    if request.htmx:
        print('htmx post')
        if request.POST.get("qstForm"):
            dateTime = datetime.now()
            ans = []
            ans.extend(request.POST.getlist('selection',''))
            count = len(ans)
            print(count)
    return render (request,"primary/nonWordReadingAccuracy.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

def testsPage (request):
    rpdnamingObj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
    rpdNamingLtrs = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
    phonemeSyllDel = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
    nonWordRepetition = NonWordRepetition.objects.filter(student_id = request.session['student'])
    nonWordReadingAccuracy = NonWordReadingAcc.objects.filter(student_id = request.session['student'])
    global context_obj
    context_obj = {} 
    global context_ltrs
    context_ltrs = {}
    global context_phoneme
    context_phoneme = {}
    global context_nonWrdRep
    context_nonWrdRep = {} 
    global context_nonWrdReading
    context_nonWrdReading = {} 
    student = Student.objects.get(id=request.session['student']).studentName

    if (rpdnamingObj.exists() or rpdNamingLtrs.exists() or phonemeSyllDel.exists() or nonWordRepetition.exists() or nonWordReadingAccuracy.exists()):
        RpdNamingObj_Score_obj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
        RpdNamingLtrs_Score_obj = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
        phonemeDel_Score_obj = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
        nonWordRep_Score_obj = NonWordRepetition.objects.filter(student_id = request.session['student'])
        nonWordReadingAcc_Score_obj = NonWordReadingAcc.objects.filter(student_id = request.session['student'])

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
                print(durationA)
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
                
                context_obj = {"rpdNOwrongA":(rpdNOwrongA),"durationA":(durationA), "totalScore_obj":(round(total)), "scoreA":(scoreA),"status_obj":('توقف '),}
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
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),"totalScore_ltr":(round(totalScore)), "durationTstA":(durationTstA),"scoreTstA":(scoreTstA),"status_ltrs":('توقف '),}
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

        if(nonWordRep_Score_obj.exists()):
            nonWordRepCorrectAns = NonWordRepetition.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWordRepCorrectAns != None):
                context_nonWrdRep = {"correctAnswers":(nonWordRepCorrectAns), "status_nonWrdRep":('منجز '), }
            else:
                context_phoneme = {"status_nonWrdRep":('غير منجز'), }
        else:
            context_nonWrdRep = {"status_nonWrdRep":('غير منجز'), }
        
        if(nonWordReadingAcc_Score_obj.exists()):
            nonWrdReadingCorrectAns = NonWordReadingAcc.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWrdReadingCorrectAns != None):
                context_nonWrdReading = {"correctAnswers":(nonWrdReadingCorrectAns), "status_nonWrdReading":('منجز '), }
            else:
                context_nonWrdReading = {"status_nonWrdReading":('غير منجز'), }
        else:
            context_nonWrdReading = {"status_nonWrdReading":('غير منجز'), }

        return render(request, "primary/testsPage.html", {"context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme":context_phoneme,"context_nonWrdRep": context_nonWrdRep,"context_nonWrdReading":context_nonWrdReading, "student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    else:
        context_obj = { "status_obj":('غير منجز'),}
        context_ltrs = { "status_ltrs":('غير منجز'),}
        context_phoneme = { "status_phoneme":('غير منجز'),}
        context_nonWrdRep= { "status_nonWrdRep":('غير منجز'),}
        context_nonWrdReading = { "status_nonWrdReading":('غير منجز'),}
        return render(request,"primary/testsPage.html", {"context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme": context_phoneme, "context_nonWrdRep": context_nonWrdRep, "context_nonWrdReading":context_nonWrdReading,"student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

def testsPageSec (request):
    phonemeSyllDelSec = PhonemeSyllableDelSec.objects.filter(student_id = request.session['student'])
    rpdnamingObjSec = RpdNamingObjSec.objects.filter(student_id = request.session['student'])
    nonWordRepetitionSec = NonWordRepetitionSec.objects.filter(student_id = request.session['student'])
    nonWordReadingAccurSec = NonWordReadingAccSec.objects.filter(student_id = request.session['student'])
    global score_phonemeDel
    score_phonemeDel = {}
    global score_obj
    score_obj = {} 
    global score_nonWrdRep
    score_nonWrdRep = {}
    global score_nonWrdReadingAcc
    score_nonWrdReadingAcc = {} 
    student = Student.objects.get(id=request.session['student']).studentName

    if (phonemeSyllDelSec.exists() or rpdnamingObjSec.exists() or nonWordRepetitionSec.exists() or nonWordReadingAccurSec.exists()):
        phonemeDel_Score_obj = PhonemeSyllableDelSec.objects.filter(student_id = request.session['student'])
        RpdNamingObj_Score_obj = RpdNamingObjSec.objects.filter(student_id = request.session['student'])
        nonWordRep_Score_obj = NonWordRepetitionSec.objects.filter(student_id = request.session['student'])
        nonWordReadingAcc_Score_obj = NonWordReadingAccSec.objects.filter(student_id = request.session['student'])
        if(phonemeDel_Score_obj.exists()):
            phonemeSyllDelAns = PhonemeSyllableDelSec.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (phonemeSyllDelAns != None):
                score_phonemeDel = {"correctAnswers":(phonemeSyllDelAns), "status_phoneme":('منجز '), }
            else:
                score_phonemeDel = {"status_phoneme":('غير منجز'), }
        else:
            score_phonemeDel = {"status_phoneme":('غير منجز'), }
        if (RpdNamingObj_Score_obj.exists()):
            rpdNOwrongA_A = RpdNamingObjSec.objects.filter(student_id = request.session['student']).latest("id")
            rpdNOwrongA = rpdNOwrongA_A.wrongAns_A
            rpdNOwrongB = RpdNamingObjSec.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            if ((rpdNOwrongA != None and rpdNOwrongB != None)):
                sttimeA=RpdNamingObjSec.objects.filter(student_id=request.session['student']).latest("id").startT_A
                ettimeA=RpdNamingObjSec.objects.filter(student_id=request.session['student']).latest("id").endT_A
                sttimeB=RpdNamingObjSec.objects.filter(student_id=request.session['student']).latest("id").startT_B
                ettimeB=RpdNamingObjSec.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durA=ettimeA-sttimeA
                durA=round(durA.total_seconds())
                print(durA)
                durB=ettimeB-sttimeB
                durB = round(durB.total_seconds())
                scrA=rpdNOwrongA+durA
                scrB=rpdNOwrongB+durB
                total=scrA+scrB
                score_obj = {"rpdNOwrongA":(rpdNOwrongA),  "rpdNOwrongB":(rpdNOwrongB), "durationA":(durA),"durationB":(durB) , "scoreA":(scrA) , "scoreB":(scrB), "totalScore_obj":(round(total)), "status_obj":('منجز '),}
            elif (rpdNOwrongA != None and rpdNOwrongB == None):
                sttimeA=RpdNamingObjSec.objects.filter(student_id=request.session['student']).latest("id").startT_A
                ettimeA=RpdNamingObjSec.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durA=ettimeA-sttimeA
                durA=round(durA.total_seconds())
                scrA=rpdNOwrongA+durA
                total=scrA
                score_obj = {"rpdNOwrongA":(rpdNOwrongA),"durationA":(durA), "totalScore_obj":(round(total)), "scoreA":(scrA),"status_obj":('توقف '),}
        else:
            score_obj = {"status_obj":('غير منجز'),}
        if( nonWordRep_Score_obj.exists()):
            nonWordRepCorrectAns = NonWordRepetitionSec.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWordRepCorrectAns != None):
                score_nonWrdRep = {"correctAnswers":(nonWordRepCorrectAns), "status_nonWrdRep":('منجز '), }
            else:
                score_nonWrdRep = {"status_nonWrdRep":('غير منجز'), }
        else:
            score_nonWrdRep = {"status_nonWrdRep":('غير منجز'), }
        if(nonWordReadingAcc_Score_obj.exists()):
            nonWrdReadingCrtAns = NonWordReadingAccSec.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWrdReadingCrtAns != None):
                score_nonWrdReadingAcc = {"correctAnswers":(nonWrdReadingCrtAns), "status_nonWrdReadingAcc":('منجز '), }
            else:
                score_nonWrdReadingAcc = {"status_nonWrdReadingAcc":('غير منجز'), }
        else:
            score_nonWrdReadingAcc = {"status_nonWrdReadingAcc":('غير منجز'), }

        return render(request, 'primary/testsPageSec.html',{"score_phonemeDel": score_phonemeDel,  "score_obj":score_obj , "score_nonWrdRep": score_nonWrdRep,"score_nonWrdReadingAcc":score_nonWrdReadingAcc ,"student":student, "examiners": Examiner.objects.get(user_id=request.user.id)})
    else:
        score_phonemeDel = { "status_phoneme":('غير منجز'),}
        score_obj = { "status_obj":('غير منجز'),}
        score_nonWrdRep= { "status_nonWrdRep":('غير منجز'),}
        score_nonWrdReadingAcc = { "status_nonWrdReadingAcc":('غير منجز'),}
        return render(request, 'primary/testsPageSec.html',{"score_phonemeDel": score_phonemeDel, "score_obj":score_obj ,"score_nonWrdRep": score_nonWrdRep,"student":(Student.objects.get(id=request.session['student']).studentName), 
        "examiners": Examiner.objects.get(user_id=request.user.id)})

@login_required(login_url="/primary/login")
def showScores(request):
    grade_2 = pd.DataFrame({
        "Percentile_Letter": ["Low","Low","Weak","Weak","Below Average","Below Average","Average","Good","Good","Superior","Superior"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],
        "RNO_Row_grade":[89,68,61,54,50,47,45,43,40,37,33],
        "RNO_Modified_standard":[46,73,82,90,95,99,102,104,108,112,117],
        "PSD_Raw_grade":[2,3,4,5,6,7,7,8,9,10,12],
        "PSD_Modified_standard":[72,77,82,87,92,96,96,101,106,111,121],
        "RNL_Raw_grade":[94,71,62,49,43,39,35,33,30,28,24],
        "RNL_Modified_standard":[48,70,78,91,96,100,104,106,109,111,115],
        "NWR_Raw_grade":[2,3,4,6,7,8,8,9,10,12,13],
        "NWR_Modified_standard":[71,75,80,88,93,97,97,101,106,114,119],
        "NWRA_Raw_grade":[2,4,5,7,9,11,13,15,17,19,22],
        "NWRA_Modified_standard":[72,77,80,85,90,95,99,104,109,114,122],
    })
    # grade3, 
    grade_3 = pd.DataFrame({
        "Percentile_Letter": ["Low","Low","Weak","Weak","Below Average","Below Average","Average","Good","Good","Superior","Superior"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],
        "RNO_Row_grade":[76,63,56,49,46,43,40,37,35,33,30],
        "RNO_Modified_standard":[53,71,80,91,94,98,102,106,109,112,116],
        "PSD_Raw_grade":[2,3,5,6,8,9,10,10,11,13,14],
        "PSD_Modified_standard":[68,73,81,85,94,98,102,102,106,115,119],
        "RNL_Raw_grade":[69,52,46,40,36,32,29,27,24,22,20],
        "RNL_Modified_standard":[51,73,81,89,94,99,103,106,110,112,115],
        "NWR_Raw_grade":[2,4,5,7,8,9,9,10,11,13,14],
        "NWR_Modified_standard":[68,77,81,90,94,98,98,102,106,115,119],
        "NWRA_Raw_grade":[2,5,7,10,13,15,16,18,19,21,23],
        "NWRA_Modified_standard":[65,73,78,86,94,99,101,106,109,114,119],
    })
    # grade_4, 
    grade_4 = pd.DataFrame({
        "Percentile_Letter": ["Low","Low","Weak","Weak","Below Average","Below Average","Average","Good","Good","Superior","Superior"],
        "Percentile_Number": [1,5,10,20,30,40,50,60,70,80,90],
        "RNO_Row_grade":[66,54,48,44,41,38,36,34,33,30,27],
        "RNO_Modified_standard":[52,72,82,89,94,101,102,106,107,112,117],
        "PSD_Raw_grade":[2,4,6,8,9,10,11,12,13,14,16],
        "PSD_Modified_standard":[64,72,80,88,92,96,100,104,108,113,121],
        "RNL_Raw_grade":[61,50,40,33,29,27,24,23,22,20,18],
        "RNL_Modified_standard":[48,65,80,91,97,100,105,106,108,111,114],
        "NWR_Raw_grade":[3,4,6,8,9,10,10,11,12,13,15],
        "NWR_Modified_standard":[68,72,81,90,94,98,98,103,107,111,120],
        "NWRA_Raw_grade":[3,5,7,11,13,15,18,19,21,22,24],
        "NWRA_Modified_standard":[66,71,76,86,91,96,104,106,111,114,119],
    })     
    # grade_5 tables
     
    grade = Student.objects.get(id=request.session['student']).grade
    if (grade == '2'):
        return_scores(grade_2,context_obj,context_phoneme,context_ltrs,context_nonWrdRep,context_nonWrdReading)
   #elif (grade == '3'):
        #return_scores(grade_3,context_obj,context_phoneme,context_ltrs,context_nonWrdRep,context_nonWrdReading)
   #elif (grade == '4'):
        #return_scores(grade_4,context_obj,context_phoneme,context_ltrs,context_nonWrdRep,context_nonWrdReading)
   #elif (grade == '5'):
        #return_scores(grade_5,context_obj,context_phoneme,context_ltrs,context_nonWrdRep,context_nonWrdReading)  
   

       


    examiner = Examiner.objects.get(user_id=request.user.id)
    age = Student.objects.get(id=request.session['student']).age
    year = age.split('/')[0]
    month = age.split('/')[1]
    day = age.split('/')[2]
    return render(request, "primary/showScores.html", {
        "students": Student.objects.get(id=request.session['student']), "examinerName": examiner.name, "context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme":context_phoneme,"context_nonWrdRep": context_nonWrdRep,"context_nonWrdReading":context_nonWrdReading, "student_age_year": year, "student_age_month": month, "student_age_day": day, "examiners": examiner})


# Secondary: test 1 training
@login_required(login_url="/primary/login")
def phonemeSyllableTrainSec(request):
    return render(request, "primary/phonemeSyllableTrainSec.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)}) 
  
# Secondary: test 1 main
@login_required(login_url="/primary/login")
def phonemeSyllableDelSec(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global testID
    global counter
    global dateTime
    global choices

    if request.POST.get("form2"):
        reason = request.POST["submitTst"]
        testResult = PhonemeSyllableDelSec.objects.create(student_id = student_instance,  correctAns = counter, reason = reason , date=dateTime)
        testResult.save()
        testID = testResult.pk
        return redirect("primary:testsPageSec")
    if request.htmx:
        if request.POST.get("form1"):
            dateTime = datetime.now()
            choices = request.POST.getlist('selection','')  
            answers = []
            answers.extend(request.POST.getlist('selection',''))
            counter = len(answers)
            print(counter)
    return render (request,"primary/phonemeSyllableDelSec.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# Secondary: test 2 part A
@login_required(login_url="/primary/login")
def rpdNamingObjSecA(request):
    student_instance = Student.objects.get(id=request.session['student'])
    print(student_instance)
    global starttime
    global endtime
    global timeWrongAns
    global number
    global test_id
    if request.POST.get("form#3"):        
        reason = request.POST["submitTst"]
        testResult = RpdNamingObjSec.objects.create(student_id = student_instance, startT_A = starttime, endT_A = endtime, wrongAns_A = number, reason_A = reason)
        testResult.save()
        test_id = testResult.pk
        if reason == "تم الانتهاء من بنود الاختبار كلها ":
            return redirect("primary:rpdNamingObjSecB")
        else:
            return redirect(reverse('primary:testsPageSec'))
    if request.htmx:
        if request.POST.get("form#1"):
            starttime = datetime.now()
            return HttpResponse('Test Started')
        if request.POST.get("form#2"):
            endtime = datetime.now()
            number = 0
            timeDif = (endtime - starttime).total_seconds()
            selectionPartA = request.POST.getlist('selection','')  
            images = []
            images.extend(request.POST.getlist('selection',''))
            counts = len(images)
            number = count
            if selectionPartA:
                timeWrongAns = timeDif + count
                return HttpResponse(timeWrongAns)
            else:
                timeWrongAns = timeDif + counts
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingObjSecA.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# Secondary: test 2 part B
@login_required(login_url="/primary/login")
def rpdNamingObjSecB(request):
    global starttime2
    global endtime2
    global number2
    global timeWrongAns2
    if request.POST.get("formtype3"):
        reason = request.POST["submitTst"]
        RpdNamingObjSec.objects.filter(id=test_id).update(startT_B = starttime2, endT_B = endtime2, wrongAns_B = number2, reason_B = reason)
        return redirect("primary:testsPageSec")
    if request.htmx:
        if request.POST.get("formtype1"):
            starttime2 = datetime.now()
            return HttpResponse('Test Started')
        if request.POST.get("formtype2"):
            endtime2 = datetime.now()
            number2 = 0
            timeDif2 = (endtime2 - starttime2).total_seconds()
            print(int(timeDif2))
            selection2 = request.POST.getlist('selection','')  
            images2 = []
            images2.extend(request.POST.getlist('selection',''))
            counts2 = len(images2)
            number2 = counts2
            if selection2:
                timeWrongAns2 = timeDif2 + counts2
                return HttpResponse(timeWrongAns2)
            else:
                timeWrongAns2 = timeDif2 + counts2
                return HttpResponse('Test Ended')
    return render(request, "primary/rpdNamingObjSecB.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)}) 

# Secondary: test 3 training
@login_required(login_url="/primary/login")
def nonWordRepTrainingSec(request):
    return render(request, "primary/nonWordRepTrainingSec.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# Secondary: test 3 
@login_required(login_url="/primary/login")
def nonWordRepSec(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global testid
    global cou
    global datee
    global selectt
    if request.POST.get("form2-3"):
        reasonDropDown = request.POST["submitTst"]
        testResult = NonWordRepetitionSec.objects.create(student_id = student_instance,  correctAns = cou, reason = reasonDropDown , date=datee)
        testResult.save()
        testid = testResult.pk
        return redirect("primary:testsPageSec")
    if request.htmx:
        print('htmx post')
        if request.POST.get("form1-3"):
            datee = datetime.now()
            selectt = request.POST.getlist('selection','')  
            choices = []
            choices.extend(request.POST.getlist('selection',''))
            cou = len(choices)
            if selectt:
                print(cou)
                return HttpResponse('Test s')
            else:
                return HttpResponse('Test Ended')
    return render (request,"primary/nonWordRepSec.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

# Secondary: test 5 
@login_required(login_url="/primary/login")
def nonWordReadingAccuracySec(request):
    student_instance = Student.objects.get(id=request.session['student'])
    global tstid
    global cnt
    global dateT

    if request.POST.get("dropDownForm"):
        reasonDropDown = request.POST["submitTst"]
        testResult = NonWordReadingAccSec.objects.create(student_id = student_instance,  correctAns = cnt, reason = reasonDropDown , date=dateT)
        testResult.save()
        tstid = testResult.pk
        return redirect("primary:testsPageSec")
    if request.htmx:
        print('htmx post')
        if request.POST.get("qstForm"):
            dateT = datetime.now()
            answrs = []
            answrs.extend(request.POST.getlist('selection',''))
            cnt = len(answrs)
            print(cnt)
    return render(request, "primary/nonWordReadingAccuracySec.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})

@login_required(login_url="/primary/login")
def showScoresSec(request):
    examiner = Examiner.objects.get(user_id=request.user.id)
    age = Student.objects.get(id=request.session['student']).age
    year = age.split('/')[0]
    month = age.split('/')[1]
    day = age.split('/')[2]
    return render(request, "primary/showScoresSec.html", {
        "students": Student.objects.get(id=request.session['student']), "examinerName": examiner.name, "score_phonemeDel": score_phonemeDel,  "score_obj":score_obj , "score_nonWrdRep": score_nonWrdRep,"score_nonWrdReadingAcc":score_nonWrdReadingAcc, "student_age_year": year, "student_age_month": month, "student_age_day": day, "examiners": examiner})

