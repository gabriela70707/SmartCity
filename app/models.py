from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    nome = models.CharField(max_length=40)

    def  __str__(self):
        return self.username

class Sensores(models.Model):  
    SENSORES = [
        ('temperatura', 'temperatura'),
        ('luminosidade', 'luminosidade'),
        ('umidade', 'umidade'),
        ('contador', 'contador')
    ]
    sensor = models.CharField(max_length=12, choices=SENSORES)

    mac_address = models.CharField(
        max_length=17,
        validators=[RegexValidator(
            regex=r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',  #exemplo de formato padrão de digitação 00:1B:44:11:3A:B9
            message="O MAC Address deve estar no formato XX:XX:XX:XX:XX:XX"
        )]
    )
    UNIDADES_MEDIDAS = [
        ('%', '%'),
        ('°C','°C'),
        ('lux', 'lux'),
        ('uni', 'uni')
    ]
    unidade_med = models.CharField(max_length=3, choices=UNIDADES_MEDIDAS) 
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField() 

    class Meta:
        verbose_name_plural = "Sensores"  #para aparecer o nome correto da tabela no admin do django 

    def __str__(self):
        return self.sensor

class Ambientes(models.Model):
    sig = models.IntegerField()
    descricao = models.CharField(max_length=100)
    ni = models.CharField(max_length=10)
    responsavel = models.CharField(max_length=70)

    class Meta:
        verbose_name_plural = "Ambientes"

    def __str__(self):
        return f"{self.sig} - {self.descricao}"



class Historico(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.SET_NULL, null=True)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.SET_NULL, null=True)
    valor = models.FloatField()
    timestamp = models.DateTimeField()  #Mudança de inteiro para data para armazenar data e hora diretamente como aparece nos arquivos excel!

    def __str__(self):
        return f"{self.sensor} - {self.valor} - {self.timestamp} - {self.ambiente}"