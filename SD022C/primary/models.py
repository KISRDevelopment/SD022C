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
        return f"{self.id}: {self.studentName}"
    
class rpdNamingObj(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_timeA = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_timeA = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    durationA = models.CharField(max_length=20, null=True)
    timeWrngAnsA = models.IntegerField(null=True)
    statusA = models.CharField(max_length=20, null=True)
    reasonA=models.CharField(max_length=60,null=True)
    start_timeB = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_timeB = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    durationB = models.CharField(max_length=20, null=True)
    timeWrngAnsB = models.IntegerField(null=True)
    statusB = models.CharField(max_length=20, null=True)
    reasonB=models.CharField(max_length=60,null=True)
