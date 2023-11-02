# REQUISIÇÃO API import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import transaction 
from hashlib import sha256
from .forms import AddUsuarioForm, RemoveUsuarioForm
from .models import Usuario

def home(request):
    return render(request, 'fortlock_app/home.html')

def cadastrar(request):
    if request.method == 'POST':
        form = AddUsuarioForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data['matricula']
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            cifra = sha256()
            cifra.update(senha.encode('utf-8'))
            senhaCifrada = cifra.hexdigest()

            try:
                if Usuario.objects.filter(matricula=matricula).exists():
                    messages.error(request, 'Matricula já em uso!')
                elif Usuario.objects.filter(email=email).exists():
                    messages.error(request, 'Email já em uso!')
                else:
                    with transaction.atomic():
                        Usuario.objects.create(matricula=matricula, nome=nome, email=email, senha=senhaCifrada)
                        messages.success(request, 'Usuário criado com sucesso.')
                        return redirect('listar')   
            
            except Exception as e:
                print(e)
                messages.error(request, f"Ocorreu um erro durante a criação do usuário: {e}")

    else:
        form = AddUsuarioForm()
    return render(request, 'fortlock_app/cadastrar.html', {'form': form})


def listar(request):
    usuarios = Usuario.objects.all()
    return render(request, 'fortlock_app/listar.html', {'usuarios': usuarios})

def remover(request):
    if request.method == 'POST':
        form = RemoveUsuarioForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data['matricula']

            try:
                with transaction.atomic():
                    usuario = Usuario.objects.get(matricula=matricula)
                    usuario.delete()
                    messages.error(request, 'Usuário removido com sucesso.')
                    return redirect('listar')

            except Usuario.DoesNotExist:
                form.add_error('matricula', "Usuário não encontrado.")

    else:
        form = RemoveUsuarioForm()
    return render(request, 'fortlock_app/remover.html', {'form': form})
