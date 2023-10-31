# REQUISIÇÃO API import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import transaction 
from hashlib import sha256
from .forms import UsuarioForm
from .models import Usuario


def pagina_inicial(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data['matricula']
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            cifra = sha256()
            cifra.update(senha.encode('utf-8'))
            senhaCifrada = cifra.hexdigest()

            try:
                with transaction.atomic():
                    Usuario.objects.create(matricula=matricula, nome=nome, email=email, senha=senhaCifrada)
            except Exception as e:
                print("Deu ruim: "+e)

            return redirect('mostrar_nome')
    else:
        form = UsuarioForm()
    return render(request, 'teste_app/pagina_inicial.html', {'form': form})


def mostrar_nome(request):
    nomes = Usuario.objects.all()
    return render(request, 'teste_app/mostrar_nome.html', {'nomes': nomes})
