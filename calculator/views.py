from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()

def index(request):
    return render(request, 'index.html')

@login_required
def calculatorView(request):
    return render(request, 'calculatorView.html')

@login_required
def history(request):
    return render(request, 'history.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if(request.POST["password1"] == request.POST["password2"]):
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"], email=request.POST["email"])
                user.save()
                login(request, user)
                return redirect("calculator")
            except IntegrityError:
                return render(request, 'signup.html', {
                    'error': "Something went wrong"
                })
        return render(request, 'signup.html', {
            'error': "Passwords do not match"
        })

def signIn(request):
    if (request.method == 'GET'):
        return render(request, 'signIn.html')
    else:
        identifier = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=identifier, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            return render(request, 'signIn.html', {'error': "Incorrect credentials"})
        else:
            login(request, user)
            return redirect("calculator")
        
def signOut(request):
    logout(request)
    return redirect("calculator")