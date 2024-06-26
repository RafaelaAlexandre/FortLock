# REQUISIÇÃO API import requests
import string
import random
import re
import threading
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.db import transaction 
from hashlib import sha256
from .forms import LoginForm, AddUsuarioForm, RemoveUsuarioForm, AddCofreForm
from .models import Usuario, Cofre
from .send_email import send_email
from datetime import datetime

# Configurações do email
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'fortlock.faeterj@gmail.com'
smtp_password = 'rbueosbvkzwvcfsq'

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

                # Obter o datetime atual
                data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

                # Obter o IP do usuário
                ip_usuario = request.META.get('REMOTE_ADDR', '')

                # Obter o agente de usuário (navegador)
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                # Criar o corpo da mensagem com informações adicionais
                body = (
                    f'Olá {usuario.nome},\n\n'
                    f'Houve um login às: {data_hora_atual}\n\n'
                    f'Informações adicionais:\n'
                    f'IP: {ip_usuario}\n'
                    f'Navegador: {user_agent}'
                )

                subject = 'Houve um login na sua conta!'
                threading.Thread(target=send_email, args=(subject, body, usuario.email)).start()

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

        valores_iniciais = {
            'matricula': usuario.matricula,
            'nome': usuario.nome,
            'email': usuario.email,
        }

        form = AddUsuarioForm(initial=valores_iniciais)
        return render(request, 'fortlock_app/dashboard/home.html', {'cofres': cofres, 'usuario': usuario, 'form': form})
        
    else:
        # O usuário não está autenticado, redirecione para a página de login
        return redirect('login')

def gerarSenha(request, idCofre):
    # Verificar se o usuário está autenticado
    user_id = request.session.get('user_id')
    if user_id is not None:
        cofre = Cofre.objects.get(pk=idCofre)
        if cofre.usuario.id == user_id:
            caracteres = string.ascii_letters + string.digits + string.punctuation
            while True:
                senhaNova = ''.join(random.choice(caracteres) for _ in range(16))

                # Verifica se a senhaNova atende aos critérios
                if any(caractere.islower() for caractere in senhaNova) and \
                    any(caractere.isupper() for caractere in senhaNova) and \
                    any(caractere.isdigit() for caractere in senhaNova) and \
                    any(caractere in string.punctuation for caractere in senhaNova):
                        break
            
            cofre.senha = senhaNova
            cofre.save()

            # Obter o datetime atual
            data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            # Criar o corpo da mensagem com informações adicionais
            body = (
                f'Olá {cofre.usuario.nome},\n\n'
                f'A nova senha do seu cofre {cofre.nome} é: {senhaNova}\n'
                f'a senha foi gerada às: {data_hora_atual}\n\n'
            )
            
            # Enviar email de forma assíncrona
            subject = 'Nova senha do cofre gerada' 
            threading.Thread(target=send_email, args=(subject, body, cofre.usuario.email)).start()

            return redirect('homeDashboard')
        
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

                # Criar o corpo da mensagem com informações adicionais
                body = (
                    f'Sentiremos sua falta :('
                )

                subject = 'Sua conta foi removida!'
                threading.Thread(target=send_email, args=(subject, body, usuario.email)).start()
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
            
            cofreNome = cofre.nome
            usuario = Usuario.objects.get(pk=request.session.get('user_id'))

            cofre.delete()
            messages.error(request, 'Cofre removido com sucesso!')

            # Obter o datetime atual
            data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            # Obter o IP do usuário
            ip_usuario = request.META.get('REMOTE_ADDR', '')

            # Obter o agente de usuário (navegador)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Criar o corpo da mensagem com informações adicionais
            body = (
                f'Olá {usuario.nome},\n\n'
                f'Seu cofre {cofreNome} foi removido às: {data_hora_atual}\n\n'
                f'Informações adicionais:\n'
                f'IP: {ip_usuario}\n'
                f'Navegador: {user_agent}'
            )

            subject = 'Seu cofre foi removido!'
            threading.Thread(target=send_email, args=(subject, body, usuario.email)).start()

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

                        # Enviar email de forma assíncrona
                        subject = 'Bem-vindo ao Fortlock'
                        body = f'Olá {nome},\n\nSua conta foi criada com sucesso! Boas vindas ao Fortlock!'
                        threading.Thread(target=send_email, args=(subject, body, email)).start()

                        return redirect('homeDashboard')   
            
            except Exception as e:
                print(e)
                messages.error(request, f"Ocorreu um erro durante a criação do usuário: {e}")

    else:
        form = AddUsuarioForm()
    return render(request, 'fortlock_app/cadastrar.html', {'form': form})

def cadastrarCofre(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        if request.method == 'POST':
            form = AddCofreForm(request.POST)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                senha = form.cleaned_data['senha']

                try:
                    with transaction.atomic():
                        cofre = Cofre.objects.create(nome=nome, senha=senha, usuario=Usuario.objects.get(pk=request.session.get('user_id')))
                        messages.success(request, 'Cofre criado com sucesso.')
                        
                        # Enviar email de confirmação de criação de cofre
                        usuario = Usuario.objects.get(pk=request.session.get('user_id'))

                        # Enviar email de forma assíncrona
                        subject = 'Cofre criado'
                        body = f'Olá {usuario.nome},\n\nSeu cofre {nome} foi criado com sucesso!'
                        threading.Thread(target=send_email, args=(subject, body, usuario.email)).start()
                        
                        return redirect('homeDashboard')   
                
                except Exception as e:
                    print(e)
                    messages.error(request, f"Ocorreu um erro durante a criação do cofre: {e}")

        else:
            form = AddCofreForm()
        return render(request, 'fortlock_app/dashboard/cadastrar.html', {'form': form})
    else:
        return redirect('login')

def editarConta(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        if request.method == 'POST':
            form = AddUsuarioForm(request.POST)
            
            usuario = Usuario.objects.get(pk=user_id)
            matricula = form.data['matricula']
            nome = form.data['nome']
            email = form.data['email']
            senha = form.data['senha']

            senhaNova = request.POST.get('senhaNova', '')

            if matricula != usuario.matricula:
                if Usuario.objects.filter(matricula=matricula).exists():
                    messages.error(request, 'Matricula já em uso!')
                    return redirect('homeDashboard')

            if email != usuario.email:
                if Usuario.objects.filter(email=email).exists():
                    messages.error(request, 'Email já em uso!')
                    return redirect('homeDashboard')

            if senhaNova:
                if len(senhaNova) < 8:
                    messages.error(request, 'A senha deve ter no mínimo 8 caracteres.')
                    return redirect('homeDashboard')

                if not any(char.isupper() for char in senhaNova):
                    messages.error(request, 'A senha deve conter pelo menos 1 letra maiúscula.')
                    return redirect('homeDashboard')

                if not any(char.islower() for char in senhaNova):
                    messages.error(request, 'A senha deve conter pelo menos 1 letra minúscula.')
                    return redirect('homeDashboard')

                if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]{};:\'",<>\./?\\|]', senhaNova):
                    messages.error(request, 'A senha deve conter pelo menos 1 caractere especial (!@#$%^&*()_+-=[]{};:\'\",<>/?.|\\).')
                    return redirect('homeDashboard')

            cifra = sha256()
            cifra.update(senha.encode('utf-8'))
            senhaCifrada = cifra.hexdigest()
            if senhaCifrada == usuario.senhaMestra:
                cifra = sha256()
                cifra.update(senhaNova.encode('utf-8'))
                senhaNovaCifrada = cifra.hexdigest()

                usuario.matricula = matricula
                usuario.nome = nome
                usuario.email = email
                usuario.senhaMestra = senhaNovaCifrada
                usuario.save()
                messages.success(request, 'Dados atualizados!')
                
                # Enviar email de forma assíncrona
                subject = 'Dados atualizados'
                body = f'Olá {usuario.nome},\n\nSeus dados foram atualizados com sucesso!'
                threading.Thread(target=send_email, args=(subject, body, usuario.email)).start()

                return redirect('homeDashboard')  
            else:
                messages.error(request, 'Senha mestra incorreta!')
                return redirect('homeDashboard')
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        return redirect('login')

def editarCofre(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        if request.method == 'POST':
            form = AddCofreForm(request.POST)
            idCofre = request.POST.get('idCofre', '') 
            nome = request.POST.get('nomeCofre', '')
            senha = request.POST.get('senhaCofre', '')

            cofre = Cofre.objects.get(pk=idCofre)
            if cofre.usuario.id == user_id:
                cofre.nome = nome
                cofre.senha = senha
                cofre.save()
                messages.success(request, 'Dados atualizados!')
                
                # Enviar email de forma assíncrona
                subject = 'Cofre atualizado'
                body = f'Olá {cofre.usuario.nome},\n\nSeu cofre {nome} foi atualizado com sucesso!'
                threading.Thread(target=send_email, args=(subject, body, cofre.usuario.email)).start()

                return redirect('homeDashboard')  
            else:
                messages.error(request, 'Você não tem permissão para editar este cofre!')
                return redirect('homeDashboard')
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        return redirect('login')
