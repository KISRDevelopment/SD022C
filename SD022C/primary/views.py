from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index (request):
    return render (request,"primary/index.html")
def help (request):
    return render (request,"primary/help.html")

def login (request):
    return render (request,"primary/login.html")

def about (request):
    return render (request,"primary/about.html")
    
def contact (request):
    return render (request,"primary/contact.html")

def requestPage (request):
    return render (request,"primary/requestPage.html")