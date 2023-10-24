from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_id')
    name = models.CharField(max_length=60)
    speciality = models.CharField(max_length=60)
    organization = models.CharField(max_length=60)

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