from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import math

from django.contrib.auth import get_user_model
from .models import LoanCalculation
User = get_user_model()



def index(request):
    return render(request, 'index.html')

@login_required
def calculatorView(request):
    if request.method == 'POST':
        try:
            data = request.POST
            tipo_calculo = data.get('tipo_calculo')
            subtipo = data.get('subtipo')
            resultado = None

            # Create a new calculation record
            calculation = LoanCalculation(
                user=request.user,
                calculation_type=tipo_calculo,
                calculation_subtype=subtipo
            )

            if tipo_calculo == 'interes':
                if subtipo == 'vp':
                    vf = float(data.get('vf', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    n = float(data.get('periodos', 0))
                    resultado = vf / ((1 + tasa) ** n)
                    calculation.vf = vf
                    calculation.tasa = tasa * 100
                    calculation.periodos = n
                elif subtipo == 'vf':
                    vp = float(data.get('vp', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    n = float(data.get('periodos', 0))
                    resultado = vp * ((1 + tasa) ** n)
                    calculation.vp = vp
                    calculation.tasa = tasa * 100
                    calculation.periodos = n
                elif subtipo == 'n':
                    vf = float(data.get('vf', 0))
                    vp = float(data.get('vp', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    resultado = math.log(vf/vp) / math.log(1 + tasa)
                    calculation.vf = vf
                    calculation.vp = vp
                    calculation.tasa = tasa * 100
                elif subtipo == 'i':
                    vf = float(data.get('vf', 0))
                    vp = float(data.get('vp', 0))
                    n = float(data.get('periodos', 0))
                    resultado = ((vf/vp) ** (1/n) - 1) * 100
                    calculation.vf = vf
                    calculation.vp = vp
                    calculation.periodos = n

            elif tipo_calculo == 'series':
                if subtipo == 'vencida':
                    a = float(data.get('renta', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    n = float(data.get('periodos', 0))
                    resultado = a * ((1 - (1 + tasa)**-n) / tasa)
                    calculation.renta = a
                    calculation.tasa = tasa * 100
                    calculation.periodos = n
                elif subtipo == 'anticipada':
                    a = float(data.get('renta', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    n = float(data.get('periodos', 0))
                    resultado = a * (1 + tasa) * ((1 - (1 + tasa)**-n) / tasa)
                    calculation.renta = a
                    calculation.tasa = tasa * 100
                    calculation.periodos = n
                elif subtipo == 'perpetua':
                    a = float(data.get('renta', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    resultado = a / tasa
                    calculation.renta = a
                    calculation.tasa = tasa * 100
                elif subtipo == 'diferida':
                    a = float(data.get('renta', 0))
                    tasa = float(data.get('tasa', 0)) / 100
                    n = float(data.get('periodos', 0))
                    k = float(data.get('gracia', 0))
                    resultado = a * ((1 - (1 + tasa)**-n) / tasa) * (1 + tasa)**-k
                    calculation.renta = a
                    calculation.tasa = tasa * 100
                    calculation.periodos = n
                    calculation.gracia = k

            # Save the result and store in database
            calculation.resultado = resultado
            calculation.save()

            return JsonResponse({
                'success': True,
                'resultado': round(resultado, 2)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

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