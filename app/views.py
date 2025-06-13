from django.shortcuts import render

#importanções de arquivos do proprio projeto
from .models import Usuario, Sensores, Historico, Ambientes
from .serializers import UsuarioSerializer, SensoresSerializer, HistoricoSerializer, AmbientesSerializer
from .permissions import IsAuthenticated

#importações de fora
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status



class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            username = request.user.username  # Obtém o usuário autenticado
            response.data['username'] = username  # Adiciona username na resposta

        return response


