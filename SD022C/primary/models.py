from django.db import models
from django.contrib.auth.models import User


# Create your models here.

STATUS_CHOICES = (
    ('ONGOING', 'Ongoing'),
    ('DONE', 'Done')
)


class Examiner(models.Model):
    STAGE_CHOICES = (
    ('PRIMARY','Primary School'),
    ('SECONDARY','Secondary School'),
    ('BOTH','Primary/Secondary')
)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_id')
    name = models.CharField(max_length=60)
    speciality = models.CharField(max_length=60)
    organization = models.CharField(max_length=60)
    stage = models.CharField(max_length=20,
                  choices=STAGE_CHOICES,
                  default="PRIMARY")

    def __str__(self):
        return f"{self.id}: {self.name}"
    
class Student(models.Model):
    examiner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='examiner_id')
    studentName = models.CharField(max_length=60)
    sex = models.CharField(max_length=60)
    schoolName = models.CharField(max_length=60)
    grade = models.CharField(max_length=60)
    civilID = models.IntegerField()
    eduDistrict = models.CharField(max_length=60)
    nationality = models.CharField(max_length=60)
    examDate = models.DateField(max_length=60)
    birthDate = models.DateField(max_length=60)
    age = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.studentName}"
    
#class Score(models.Model):
    #student = models.ForeignKey(Student, on_delete=models.CASCADE)
    #rpdNOA_startT = models.DateTimeField(null=True)
    #rpdNOA_endT = models.DateTimeField(null=True)
    #rpdNOA_wrongAns = models.IntegerField(null=True)
    #rpdNOA_reason=models.CharField(max_length=60,null=True)
    #rpdNOB_startT = models.DateTimeField(null=True)
    #rpdNOB_endT = models.DateTimeField(null=True)
    #rpdNOB_wrongAns = models.IntegerField(null=True)
    #rpdNOB_reason=models.CharField(max_length=60,null=True)
    #rpdNLA_startT = models.DateTimeField(null=True)
    #rpdNLA_endT = models.DateTimeField(null=True)
    #rpdNLA_wrongAns = models.IntegerField(null=True)
    #rpdNLA_reason=models.CharField(max_length=60,null=True)
    #rpdNLB_startT = models.DateTimeField(null=True)
    #rpdNLB_endT = models.DateTimeField(null=True)
    #rpdNLB_wrongAns = models.IntegerField(null=True)
    #rpdNLB_reason=models.CharField(max_length=60,null=True)

#The Test name 
class Test(models.Model):
    student_id = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = 'student_id')
    test_name = models.CharField(max_length=60, unique = False, null = True)

    def __str__(self):
        return f"{self.id}: {self.student_id} {self.test_name}"
    
#Test Parts such as part A part B etc (students can take as many tests part and it will be saved)
class Score(models.Model):
    test_id = models.ForeignKey(Test, on_delete = models.CASCADE, related_name = 'test_id' , null=True)
    parts_name = models.CharField(max_length=60, unique = False, null = True)
    startT = models.DateTimeField(null=True)
    endT = models.DateTimeField(null=True)
    wrongAns = models.IntegerField(null=True)
    reason=models.CharField(max_length=60,null=True)

    def __str__(self):
        return f"{self.id}: {self.test_id.student_id} | {self.test_id} | {self.parts_name}"

