from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login as login_django
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


# Create your views here.
@login_required(login_url="/cafe/login_user/")
def configuracao(request):
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

            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Senha ou nome incorretos.'})
    else:
        return render(request, 'login.html')

@login_required(login_url="/cafe/login_user/")
def home_page(request):
    return render(request, 'home.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def trocar_senha(request):
    if request.method == 'POST':
        senha_antiga = request.POST.get('senhaantiga')
        senha_nova = request.POST.get('senhanova')
        senha_confirmacao = request.POST.get('senhaconfirmacao')

        user =  request.user
        if not user.check_password(senha_antiga):
            print('oi3')
            return render(request, 'componente/alerta.html', {'error': ' Senha antiga incorreta'})
        if senha_nova != senha_confirmacao:
            print('oiu')
            return render(request, 'componente/alerta.html', {'error': 'As senhas não coincidem'})
        print('oi')
        user.set_password(senha_nova)
        user.save()
        update_session_auth_hash(request, user)
        return render(request, 'componente/alerta.html', {'sucesso': 'Senha atualizada'})
    return render(request, 'configuracao.html')