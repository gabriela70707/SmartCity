from django.urls import path
from .views import SensoresListCreateAPIView,SensoresDetailAPIView,LoginView, AmbientesListCreateAPIView, AmbientesDetailAPIView,HistoricoListCreateAPIView,HistoricoDetailAPIView,UpdateSensorStatusAPIView,ImportExcelAPIView,ExportExcelAPIView

urlpatterns = [
    path('token/', LoginView.as_view()),  # Para o usuario realizar login

    #SENSORES
    path('sensores/', SensoresListCreateAPIView.as_view()),  # Para listar e criar sensores
    path('sensores/<int:pk>/', SensoresDetailAPIView.as_view()),  # Busca, atualiza e deleta sensores por ID
    path('sensores/<int:pk>/status/', UpdateSensorStatusAPIView.as_view()),  # Atualizar status do sensor
    
    #AMBIENTES
    path('ambientes/', AmbientesListCreateAPIView.as_view()),  # Para listar e criar ambientes
    path('ambientes/<int:pk>/', AmbientesDetailAPIView.as_view()),  # Para buscar, atualizar e deletar ambientes

    #HISTORICO 
    path('historico/', HistoricoListCreateAPIView.as_view()),  # Para listar e criar registros históricos
    path('historico/<int:pk>/', HistoricoDetailAPIView.as_view()),  # Para buscar, atualizar e deletar registros históricos

    #EXCEL
    path('import-excel/', ImportExcelAPIView.as_view()),  # Importar dados via Excel
    path('export-excel/', ExportExcelAPIView.as_view()),  # Rota para exportação
]
