from django.contrib import admin
from .models import Examiner
from .models import Student
from .models import rpdNamingObj
# Register your models here.
admin.site.register(Examiner)
admin.site.register(Student)
admin.site.register(rpdNamingObj)
