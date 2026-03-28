from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Aqui definimos as colunas que aparecem na tabela do Admin
    list_display = ('get_first_name', 'user', 'phone')
    
    # Função para pegar o nome salvo no User relacionado
    def get_first_name(self, obj):
        # Retorna o first_name se existir, senão retorna o username
        return obj.user.first_name if obj.user.first_name else obj.user.username
    
    # Define o título da coluna na interface
    get_first_name.short_description = 'Nome do Cidadão'
    
    # Permite clicar no nome para editar o perfil
    list_display_links = ('get_first_name', 'user')