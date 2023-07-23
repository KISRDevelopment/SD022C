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
]