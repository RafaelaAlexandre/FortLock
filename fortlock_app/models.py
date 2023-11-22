from django.db import models


# Create your models here.
class Usuario(models.Model):
    matricula = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    senhaMestra = models.CharField(max_length=30)

    def __str__(self):
        return self.nome  # Defina como deseja que o usuário seja representado


class Cofre(models.Model):
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nome  # Define o nome do cofre
