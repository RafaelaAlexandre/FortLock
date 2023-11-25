from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('dashboard/', views.homeDashboard, name='homeDashboard'),
    path('gerarSenha/<int:idCofre>/', views.gerarSenha, name='gerarSenha'),
    path('removerConta/', views.removerConta, name='removerConta'),
    path('removerCofre/', views.removerCofre, name='removerCofre'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('cadastrarCofre/', views.cadastrarCofre, name='cadastrarCofre'),
    path('editarConta/', views.editarConta, name='editarConta'),
    path('listar/', views.listar, name='listar'),
    path('remover/', views.remover, name='remover'),
]
