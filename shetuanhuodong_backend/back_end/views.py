from django.shortcuts import render
# from django import HttpResponse
from django.http import HttpResponse

# Create your views here.
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    return HttpResponse({'username': username, 'password': password})


