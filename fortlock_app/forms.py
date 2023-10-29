from django import forms


class NomeForm(forms.Form):
    nome = forms.CharField(label='Seu nome', max_length=100)