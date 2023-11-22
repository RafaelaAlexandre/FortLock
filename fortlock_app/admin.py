# Em meu_app/admin.py
from django.contrib import admin
from .models import Usuario, Cofre

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'email')  # Adicione os campos desejados
    list_filter = ('nome', 'matricula')  # Adicione os campos desejados como filtros

@admin.register(Cofre)
class CofreAdmin(admin.ModelAdmin):
    list_display = ('nome', 'senha', 'usuario')  # Adicione os campos desejados
    list_filter = ('usuario',)  # Adicione os campos desejados como filtros
