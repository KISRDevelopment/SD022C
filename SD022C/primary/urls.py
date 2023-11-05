from django.urls import path
from . import views
app_name="primary" 
urlpatterns = [
    path("",views.index,name="index"),
    path("help",views.help, name="help"),
    path("login",views.login, name="login"),
    path("about",views.about, name="about"),
    path("contact",views.contact, name="contact"),
    path("requestPage",views.requestPage, name="requestPage"),
    path("adminPage",views.adminPage, name="adminPage"),
    path("superusers",views.superusers, name="superusers"),
    path("signupSuperUser",views.signupSuperUser, name="signupSuperUser"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('logout/', views.logout, name='logout'),
    path('examinerPage/', views.examinerPage, name='examinerPage'),
    path('profile/', views.profile, name='profile'),
    path('students/', views.students, name='students'),
    path('signupStudents/', views.signupStudents, name='signupStudents'),
    path('deleteStudent/<int:id>', views.deleteStudent, name='deleteStudent'),
    path('testsPage/', views.testsPage, name='testsPage'),
    path('startTest/', views.startTest, name='startTest'),
    path('rapidNamingObj/', views.rapidNamingObj, name='rapidNamingObj'),
    #path('editStudent/<int:id>', views.editStudent, name='editStudent'),

    #path('password/<int:id>', views.password, name='password'),
]