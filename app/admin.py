from django.contrib import admin
from .models import Usuario, Sensores, Ambientes, Historico
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    pass

class SensoresAdmin(admin.ModelAdmin):
    list_filter = ('id','sensor')  #adiciona uma filtragem para visualização dos dados na pagina de admin

class HistoricoAdmin(admin.ModelAdmin):
    list_filter = ('timestamp', 'id')

class AmbientesAdmin(admin.ModelAdmin):
    list_filter = ('sig',) #a virgula garante que seja interpretado como uma tupla(não tirar ela)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Sensores, SensoresAdmin)
admin.site.register(Ambientes, AmbientesAdmin)
admin.site.register(Historico, HistoricoAdmin)

