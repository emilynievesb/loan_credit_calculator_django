from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

@login_required
def calculatorView(request):
    return render(request, 'calculatorView.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if(request.POST["password1"] == request.POST["password2"]):
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("calculator")
            except IntegrityError:
                return render(request, 'signup.html', {
                    'error': "Username already exists"
                })
        return render(request, 'signup.html', {
            'error': "Passwords do not match"
        })

def signIn(request):
    if(request.method == 'GET'):
        return render(request, 'signIn.html')
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signIn.html', {
                'error': "Incorrect username or password"
            })
        else:
            login(request, user)
            return redirect("calculator")
        
def signOut(request):
    logout(request)
    return redirect("calculator")