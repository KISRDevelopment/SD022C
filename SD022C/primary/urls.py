from django.urls import path
from . import views
app_name="primary" 
urlpatterns = [
    path("",views.index,name="index"),
    path("help",views.help, name="help"),
    path("login",views.login, name="login"),
    path("about",views.about, name="about"),
    path("contact",views.contact, name="contact"),
]