from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('mostrar_nome/', views.mostrar_nome, name='mostrar_nome'),
]
