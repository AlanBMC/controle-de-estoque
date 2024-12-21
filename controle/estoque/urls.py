from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.cadastro_usuario, name='login'),
    path('login_user/', views.login_user, name='login_user'),
]
