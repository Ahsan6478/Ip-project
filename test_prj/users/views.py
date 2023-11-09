# from django.shortcuts import render
from django.http import HttpResponse
from ipware import get_client_ip




def index(request):  
    
    return HttpResponse("<h1>Welcome User!</h1> ")
    