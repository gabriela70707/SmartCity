from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=40)

    def  __str__(self):
        return self.username

class Sensores(models.Model):
    sensor = models.CharField(max_length=40)
    mac_address = models.CharField(max_length=17)
    unidade_med = models.CharField(max_length=3)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField()

    def __str__(self):
        return self.sensor

class Ambientes(models.Model):
    sig = models.IntegerField()
    descricao = models.CharField(max_length=100)
    ni = models.CharField(max_length=10)
    responsavel = models.CharField(max_length=70)

    def __str__(self):
        return self.sig


class Historico(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.SET_NULL, null=True)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.SET_NULL, null=True)
    valor = models.FloatField()
    timestamp = models.IntegerField()

    def __str__(self):
        return f"{self.sensor} - {self.valor} - {self.timestamp}"