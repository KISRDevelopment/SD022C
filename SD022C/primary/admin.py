from django.contrib import admin
from .models import Examiner
from .models import Student
from .models import Score
# Register your models here.
admin.site.register(Examiner)
admin.site.register(Student)
admin.site.register(Score)
