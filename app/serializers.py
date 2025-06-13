#Esse arquivo transforma objetos do banco de dados em formato JSON ermitindo que os dados sejam facilmente enviados e recebidos pela API Django REST Framework.
from rest_framework import serializers
from .models import Usuario, Sensores, Ambientes, Historico

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class SensoresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensores
        fields = '__all__'


class AmbientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambientes
        fields = '__all__'

class HistoricoSerializer(serializers.ModelSerializer):
    sensor_id = serializers.IntegerField(source="sensor.id", read_only=True)  # ID do sensor
    sensor_nome = serializers.CharField(source="sensor.sensor", read_only=True)  # Nome do sensor
    ambiente_descricao = serializers.CharField(source="ambiente.descricao", read_only=True) # Descrição do ambiente
    ambiente_id = serializers.IntegerField(source="ambiente.id", read_only=True)  # ID do ambiente

    class Meta:
        model = Historico
        fields = ['id', 'sensor_id', 'sensor_nome', 'ambiente_id', 'ambiente_descricao', 'valor', 'timestamp']



"""

Filtro HIstorico
query_parans -> sensor=temperatura

if sensor:
   sensores = Sensor.objects.filter(sensor=sensor).values_list('id', flat=True)
   [1,2,335,7,8,1]

   queryset = queryset.filter(sensor__in = sensores)

   
SELECT * FROM historico WHERE sensor in (SELECT id FROM SENSORES WHERE sensor='temperatura');




"""