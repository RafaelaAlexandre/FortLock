import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from hashlib import sha256
from .forms import NomeForm
from .models import Usuario


def pagina_inicial(request):
    if request.method == 'POST':
        form = NomeForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            Usuario.objects.create(nome=nome, matricula='MATRICULAEXEMPLO', email='email@example.com', senha='senhaDIFICIL')
            return redirect('mostrar_nome')
    else:
        form = NomeForm()
    return render(request, 'teste_app/pagina_inicial.html', {'form': form})


def mostrar_nome(request):
    nomes = Usuario.objects.all()
    return render(request, 'teste_app/mostrar_nome.html', {'nomes': nomes})
