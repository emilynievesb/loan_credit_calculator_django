from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError

# Create your views here.

def index(request):
    return render(request, 'index.html')

def calculatorView(request):
    return render(request, 'calculatorView.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if(request.POST["password1"] == request.POST["password2"]):
            #regiter User
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("calculator")
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "Username already exists"
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Passwords do not match"
        })

def signIn(request):
    if(request.method == 'GET'):
        return render(request, 'signIn.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signIn.html', {
                'form': AuthenticationForm,
                'error': "Incorrect username or password"
            })
        else:
            login(request, user)
            return redirect("calculator")
        
def signOut(request):
    logout(request)
    return redirect("calculator")