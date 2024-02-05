from django.contrib import admin
from .models import Examiner
from .models import Student
#from .models import Score
from .models import *
# Register your models here.
admin.site.register(Examiner)
admin.site.register(Student)
admin.site.register(RpdNamingObj_Score)
admin.site.register(RpdNamingLtrs_Score)
admin.site.register(PhonemeSyllableDel)
admin.site.register(NonWordRepetition)
admin.site.register(NonWordReadingAcc)


