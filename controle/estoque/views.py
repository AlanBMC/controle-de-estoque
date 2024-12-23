from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth import login as login_django
from .models import Usuario, Produto, Fornecedor, MovimentoEstoque
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


# Create your views here.
@login_required(login_url="/cafe/login_user/")
def configuracao(request):
    usuarios = lista_usuarios(request)
    usuario_atual = get_object_or_404(Usuario, id=request.user.id)
    return render(request, 'configuracao.html', {'users': usuarios , 'usuario_atual':usuario_atual.tipo_user }) 

def view_produto(request):
    if request.method == 'GET':
        return render(request, 'produto.html')

def cria_produto(request):
    if request.method == 'POST': 
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade')
        vencimento = request.POST.get('vencimento')
        fornecedor_id = request.POST.get('fornecedor')


        _, admin_atual = usuario_atual(request)

def usuario_atual(request):
    '''
    Funcionalidade: retorna usuario-adm / evitar linhas de codigos
    Parametro: request
    Retorna uma tupla: usuario_atual, admin_responsavel
    '''
    usuario_atual = Usuario.objects.filter(nome=request.user.username).first()
    admin_responsavel = usuario_atual.criado_por if usuario_atual.criado_por else usuario_atual
    return usuario_atual, admin_responsavel


@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        tipo_user = request.POST.get('tipo_user')

        usuario.nome = nome
        usuario.tipo_user = tipo_user
        usuario.save()

        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('configuracao')  # Redireciona para a tela de configuração
    
    return redirect('configuracao') 


@login_required
def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    admin_usuario = Usuario.objects.filter(nome=request.user.username).first()  # Converte para Usuario

    print(usuario.criado_por.id)  # Depuração
    print('usuario request', admin_usuario.id)  # Depuração
    
    if usuario.criado_por == admin_usuario or request.user.is_superuser:
        usuario.delete()
        print('excluído')
        messages.success(request, 'Usuário excluído com sucesso!')
    else:
        print('sem permissão')
        messages.error(request, 'Você não tem permissão para excluir este usuário.')

    return redirect('configuracao')


@login_required(login_url="/cafe/login_user/")
def lista_usuarios(request):
    # Obter o Usuario correspondente ao User logado
    admin_usuario = Usuario.objects.filter(nome=request.user.username).first()

    if not admin_usuario:
        return render(request, 'componentes/alerta.html', {
            'error': 'Você precisa ser admin para visualizar os usuários.'
        })

    # Filtrar apenas os usuários criados por este admin
    usuarios = Usuario.objects.filter(criado_por=admin_usuario)

    return  usuarios


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

@login_required(login_url="/cafe/login_user/")
def cria_novo_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirmasenha')
        tipo_user = request.POST.get('tipouser')
        admin_usuario = Usuario.objects.filter(nome=request.user.username, tipo_user='admin').first()
        print(admin_usuario)
        if not admin_usuario:
            return render(request, 'componente/alerta.html', {'error': 'Voce precisa ser admin.'})
        if senha != confirma_senha:
            return render(request, 'componente/alerta.html', {'error': 'Senhas não coincidem.'})
        
        if User.objects.filter(username=nome):
            return render(request, 'componente/alerta.html', {'error': 'Usuario ja existe'})
        else:
            user = User.objects.create_user(username=nome, password=senha)
            user.save()
            usuario = Usuario(nome=nome, tipo_user=tipo_user, criado_por=admin_usuario )
            usuario.save()
            return render(request, 'componente/alerta.html', {'sucesso': 'Usuario cadastrado'})

def editar_nome_usuario(request):
    
    usuario = get_object_or_404(Usuario, nome=request.user.username) 
    if request.method == 'POST':
        novo_nome =  request.POST.get('novoNome')
        if  User.objects.filter(username=novo_nome).exclude(id=request.user.id).exists():
            print('entrou aqui quando deu erro')
            return render(request, 'componente/alerta.html', {'error': 'Nome ja existe'})
        else:
            user = request.user
            user.username = novo_nome
            user.save()
            usuario.nome = novo_nome
            usuario.save()
            print('entrou aqui foi deu 200')
            return render(request, 'componente/alerta.html', {'sucesso': 'Nome editado com sucesso'})




def deleta_usuario(request):
    pass

@login_required(login_url="/cafe/login_user/")
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