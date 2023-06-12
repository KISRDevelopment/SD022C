from django.urls import path
from . import views
app_name="homePage" 
urlpatterns = [
    path("",views.index,name="index"),
    path("help",views.help, name="help"),
    path("login",views.login, name="login"),

]