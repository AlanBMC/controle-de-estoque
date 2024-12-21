from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro'),
    path('login_user/', views.login_user, name='login'),
]
