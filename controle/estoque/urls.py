from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('configuracao/', views.configuracao, name='configuracao'),
    path('login_user/', views.login_user, name='login'),
    path('home/', views.home_page, name='home'),
    path('troca_senha/', views.trocar_senha, name='trocasenha'),
    path('cria_novo_usuario/', views.cria_novo_usuario, name='cria_novo_usuario'),
    path('editar_nome_usuario/' , views.editar_nome_usuario, name='editar_nome_usuario'),
    path('excluir_usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('view_produto/', views.view_produto, name='view_produto'),
    path('cria_fornecedor/', views.cria_fornecedor, name='cria_fornecedor'),

]
