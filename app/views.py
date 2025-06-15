#Nesse arquivo fica a logica das funções da API

#importações de fora
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
import pandas as pd
from django.core.exceptions import ValidationError
import io   
from django.http import HttpResponse
from django.http import FileResponse
import os

#importanções de arquivos do proprio projeto
from .models import Usuario, Sensores, Historico, Ambientes
from .serializers import UsuarioSerializer, SensoresSerializer, HistoricoSerializer, AmbientesSerializer
from .permissions import IsAuthenticated

#LOGIN
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK and request.user.is_authenticated:
            response.data['username'] = request.user.username  # Adiciona username na resposta
        else:
            response.data['username'] = None  # Evita erro caso o usuário não esteja autenticado

        return response

#CRUD DE SENSORES
class SensoresListCreateAPIView(ListCreateAPIView):
    """Lista sensores e permite criar novos, com filtros."""
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtra sensores por tipo e status."""
        queryset = Sensores.objects.all()
        sensor_tipo = self.request.query_params.get("sensor")  # Ex: sensor=Temperatura:  /sensores/?sensor=Temperatura
        status_filtro = self.request.query_params.get("status")  # Ex: status=true ou false:  /sensores/?status=true


        if sensor_tipo:
            queryset = queryset.filter(sensor=sensor_tipo)
        if status_filtro is not None:
            queryset = queryset.filter(status=status_filtro.lower() == "true")

        return queryset

    def create(self, request, *args, **kwargs):
        """Criação de sensor com mensagens de erro personalizadas."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sensor criado com sucesso!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Erro ao criar sensor", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SensoresDetailAPIView(RetrieveUpdateDestroyAPIView):
    """Busca, atualiza e deleta sensores por ID."""
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """Atualização de sensor com validação de erro."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sensor atualizado com sucesso!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Erro ao atualizar sensor", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Exclusão de sensor com feedback."""
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Sensor deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)


#ATUALIZAR O STATUS DO SENSOR DE FORMA MAIS OBJETIVA
class UpdateSensorStatusAPIView(APIView):
    """Atualiza o status de um sensor (ativo/inativo)."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        sensor = get_object_or_404(Sensores, pk=pk)
        novo_status = request.data.get("status")

        if novo_status is None:
            return Response({"error": "Status não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        sensor.status = bool(novo_status)
        sensor.save()

        return Response({"message": "Status do sensor atualizado!", "status": sensor.status}, status=status.HTTP_200_OK)


#CRUD DE AMBIENTES
class AmbientesListCreateAPIView(ListCreateAPIView):
    """Lista todos os ambientes e permite criar novos."""
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Criação de ambiente com mensagens de erro personalizadas."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ambiente criado com sucesso!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Erro ao criar ambiente", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AmbientesDetailAPIView(RetrieveUpdateDestroyAPIView):
    """Busca, atualiza e deleta ambientes por ID."""
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """Atualização de ambiente com validação de erro."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ambiente atualizado com sucesso!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Erro ao atualizar ambiente", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Exclusão de ambiente com feedback."""
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Ambiente deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

#CRUD DE HISTORICO
class HistoricoListCreateAPIView(ListCreateAPIView):
    """Lista registros históricos e permite criar novos, com filtros."""
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtra por tipo de sensor e por intervalo de datas."""
        queryset = Historico.objects.all()
        sensor_tipo = self.request.query_params.get("sensor")  # Ex: sensor=Temperatura
        data_inicio = self.request.query_params.get("data_inicio")  # Ex: data_inicio=2025-06-01
        data_fim = self.request.query_params.get("data_fim")  # Ex: data_fim=2025-06-15

        if sensor_tipo:
            queryset = queryset.filter(sensor__sensor=sensor_tipo)
        if data_inicio and data_fim:
            queryset = queryset.filter(timestamp__range=[data_inicio, data_fim])

        return queryset

    def create(self, request, *args, **kwargs):
        """Criação de histórico com mensagens de erro."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registro histórico criado com sucesso!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Erro ao criar registro histórico", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HistoricoDetailAPIView(RetrieveUpdateDestroyAPIView):
    """Busca, atualiza e deleta registros históricos por ID."""
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """Atualização de histórico com validação de erro."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registro histórico atualizado com sucesso!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Erro ao atualizar registro histórico", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Exclusão de registro histórico com feedback."""
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Registro histórico deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)


#IMPORTAÇÃO DE DADOS EXCEL 
class ImportExcelAPIView(APIView):
    """Recebe um arquivo Excel e importa os dados para o banco."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "Nenhum arquivo enviado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip()  # Remove espaços extras

            # Validando a presença das colunas necessárias
            required_columns = {
                "Sensores": ["sensor", "mac_address", "unidade_med", "latitude", "longitude", "status"],
                "Ambientes": ["sig", "descricao", "ni", "responsavel"],
                "Historico": ["sensor_id", "ambiente_id", "valor", "timestamp"]
            }

            # Identifica qual modelo importar baseado nas colunas disponíveis
            if set(df.columns.tolist()).issuperset(required_columns["Sensores"]):
                model = Sensores
                msg = "Sensores importados"
            elif set(df.columns.tolist()).issuperset(required_columns["Ambientes"]):
                model = Ambientes
                msg = "Ambientes importados"
            elif set(df.columns.tolist()).issuperset(required_columns["Historico"]):
                model = Historico
                msg = "Histórico importado"
            else:
                return Response({
                    "error": f"Formato de arquivo inválido. Colunas encontradas: {df.columns.tolist()}"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Verificando se os IDs de sensor e ambiente existem antes da importação
            sensor_ids_validos = set(Sensores.objects.values_list("id", flat=True))
            ambiente_ids_validos = set(Ambientes.objects.values_list("id", flat=True))

            # Filtrando os registros inválidos antes do bulk_create
            df = df[df["sensor_id"].isin(sensor_ids_validos)]
            df = df[df["ambiente_id"].isin(ambiente_ids_validos)]

            # Convertendo status para booleano apenas se a coluna existir
            if "status" in df.columns:
                df["status"] = df["status"].replace({"ativo": True, "inativo": False})



            # Criar registros no banco com tratamento de erro
            try:
                objs = [model(**row.to_dict()) for _, row in df.iterrows()]
                model.objects.bulk_create(objs)
            except Exception as e:
                return Response({"error": f"Erro ao inserir registros: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": msg, "total": len(objs)}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Erro ao processar o arquivo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class ExportExcelAPIView(APIView):
    """Exporta dados de Sensores, Ambientes e Histórico para um arquivo Excel."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Criar um arquivo Excel em memória
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine="openpyxl")

        # Criar DataFrames com os dados do banco
        df_sensores = pd.DataFrame(list(Sensores.objects.values()))
        df_ambientes = pd.DataFrame(list(Ambientes.objects.values()))
        df_historico = pd.DataFrame(list(Historico.objects.values()))

        # **Corrige o problema de timezone nos timestamps**
        if "timestamp" in df_historico.columns:
            df_historico["timestamp"] = pd.to_datetime(df_historico["timestamp"]).dt.tz_localize(None)

        # Escrever cada dataset em uma aba do Excel
        df_sensores.to_excel(writer, sheet_name="Sensores", index=False)
        df_ambientes.to_excel(writer, sheet_name="Ambientes", index=False)
        df_historico.to_excel(writer, sheet_name="Historico", index=False)

        writer.close()
        output.seek(0)

        # Criar resposta HTTP para download do arquivo
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="dados_smartcity.xlsx"'
        return response


#PERMITIR QUE O USUARIO BAIXE UM ARQUIVO MODELO PARA PREENCHER OS DADOS
class DownloadExcelModeloAPIView(APIView):
    """Permite baixar os modelos de Excel pré-formatados."""
    permission_classes = [IsAuthenticated]

    def get(self, request, nome_arquivo):
        # Caminho da pasta `modelos`
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modelos")
        file_path = os.path.join(base_path, nome_arquivo)

        if not os.path.exists(file_path):
            return Response({"error": "Modelo não encontrado"}, status=404)

        return FileResponse(open(file_path, "rb"), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")