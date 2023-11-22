# REQUISIÇÃO API import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import transaction 
from hashlib import sha256
from .forms import LoginForm, AddUsuarioForm, RemoveUsuarioForm
from .models import Usuario, Cofre

def home(request):
    return render(request, 'fortlock_app/home.html')

def userLogin(request):
    # Verificar se o usuário está autenticado
    if 'user_id' in request.session:
        # O usuário está autenticado, redirecione para a página inicial
        return redirect('homeDashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            cifra = sha256()
            cifra.update(senha.encode('utf-8'))
            senhaCifrada = cifra.hexdigest()

            try:
                usuario = Usuario.objects.get(email=email, senhaMestra=senhaCifrada)
                # Exemplo: Armazenar o ID do usuário na sessão
                request.session['user_id'] = usuario.id

                return redirect('homeDashboard')
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciais inválidas. Tente novamente.')
    else:
        form = LoginForm()
    return render(request, 'fortlock_app/login.html', {'form': form})

def userLogout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')

def homeDashboard(request):
    # Verificar se o usuário está autenticado
    user_id = request.session.get('user_id')
    if user_id is not None:
        # O usuário está autenticado, continue com a lógica da view
        usuario = Usuario.objects.get(pk=user_id)
        cofres = Cofre.objects.filter(usuario=usuario)
        return render(request, 'fortlock_app/dashboard/home.html', {'cofres': cofres, 'usuario': usuario})
        
    else:
        # O usuário não está autenticado, redirecione para a página de login
        return redirect('login')

def removerConta(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        if request.method == 'POST':
            usuario = Usuario.objects.get(pk=user_id)
            senha = request.POST.get('senha', '')
            cifra = sha256()
            cifra.update(senha.encode('utf-8'))
            senhaCifrada = cifra.hexdigest()
            if senhaCifrada == usuario.senhaMestra:
                usuario.delete()
                return redirect('logout') 
            else:
                messages.error(request, 'Senha incorreta!')
                return redirect('homeDashboard')
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        return redirect('login')

def removerCofre(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            cofre = request.POST.get('cofre', '')
            cofre = Cofre.objects.get(pk=cofre)
            cofre.delete()
            return redirect('homeDashboard') 
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        return redirect('login')

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
                        usuario = Usuario.objects.create(matricula=matricula, nome=nome, email=email, senhaMestra=senhaCifrada)
                        messages.success(request, 'Usuário criado com sucesso.')
                        if 'user_id' in request.session:
                            del request.session['user_id']
                        request.session['user_id'] = usuario.id
                        return redirect('homeDashboard')   
            
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
