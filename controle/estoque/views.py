from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login as login_django
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse


# Create your views here.
def cadastro_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        if User.objects.filter(username=nome):
            
            return render(request, 'componente/alerta.html', {'error': 'Usuario ja existe'})
        else:
            user = User.objects.create_user(username=nome, password=senha)
            user.save()
            usuario = Usuario(nome=nome, tipo_user='admin')
            usuario.save()
            return render(request, 'componente/alerta.html', {'sucesso': 'Usuario cadastrado'})
            #redirecionar para login
    else:
        return render(request, 'configuracao.html') 

def login_user(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome, password=senha)
        if user:
            login_django(request, user)
            return render(request, 'home.html')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login_user')

