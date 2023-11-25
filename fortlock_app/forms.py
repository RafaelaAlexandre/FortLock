import re
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(label='Seu e-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Seu senha mestra', max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError as e:
                self.add_error('email', "Endereço de e-mail inválido.\n"+e)
        return email

class AddUsuarioForm(forms.Form):
    matricula = forms.CharField(label='Sua matrícula', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nome = forms.CharField(label='Seu nome', max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Seu e-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Sua senha mestra', max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError as e:
                self.add_error('email', "Endereço de e-mail inválido.\n"+e)
        return email

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if senha:
            if len(senha) < 8:
                raise ValidationError("A senha deve ter no mínimo 8 caracteres.")

            if not any(char.isupper() for char in senha):
                raise ValidationError("A senha deve conter pelo menos 1 letra maiúscula.")

            if not any(char.islower() for char in senha):
                raise ValidationError("A senha deve conter pelo menos 1 letra minúscula.")

            if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]{};:\'",<>\./?\\|]', senha):
                raise ValidationError("A senha deve conter pelo menos 1 caractere especial (!@#$%^&*()_+-=[]{};:'\",<>/?.|\\).")

        return senha

class RemoveUsuarioForm(forms.Form):
    matricula = forms.CharField(label='Matricula:', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class AddCofreForm(forms.Form):
    nome = forms.CharField(label='Nome do cofre', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label='Senha do cofre', max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
