import re
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UsuarioForm(forms.Form):
    matricula = forms.CharField(label='Sua matrícula', max_length=30, required=True)
    nome = forms.CharField(label='Seu nome', max_length=50, required=True)
    email = forms.EmailField(label='Seu e-mail', required=True)
    senha = forms.CharField(label='Seu senha', max_length=30, required=True)

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

            if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]{};:\'",<>\./?\\|]$', senha):
                raise ValidationError("A senha deve conter pelo menos 1 caractere especial (!@#$%^&*()_+-=[]{};:'\",<>/?.|\\).")

        return senha