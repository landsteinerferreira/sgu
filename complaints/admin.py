from django.contrib import admin
from django.utils.html import format_html
from complaints.models import Category, Complaints, Suggestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    # Exibição na lista principal
    list_display = (
        'id_protocolo', 
        'title', 
        'sector', 
        'status',           # Necessário para list_editable
        'priority',         # Necessário para list_editable
        'status_badge', 
        'priority_badge', 
        'user', 
        'created_at'
    )
    
    list_editable = ('status', 'priority')
    list_filter = ('status', 'priority', 'sector', 'category', 'created_at')
    search_fields = ('title', 'description', 'address', 'user__username')
    list_per_page = 20

    # Organização por Abas (Fieldsets)
    fieldsets = (
        ('Dados do Cidadão', {
            'fields': (('user', 'category'), 'title', 'description', 'photo_view'),
        }),
        ('Localização', {
            'fields': ('sector', 'address', 'location'), # ADICIONADO 'location' aqui
            'description': 'O mapa abaixo indica a posição exata da ocorrência.',
        }),
        ('Ação da Prefeitura', {
            'fields': ('priority', 'status', 'feedback_agency'),
        }),
    )

    # Campos que o administrador não pode alterar manualmente
    readonly_fields = ('user', 'title', 'description', 'category', 'photo_view', 'created_at')

    # --- Funções Visuais ---
    
    def id_protocolo(self, obj):
        return format_html("<b>#{}</b>", obj.id)
    id_protocolo.short_description = 'Prot.'

    def status_badge(self, obj):
        colors = {'OPEN': 'warning', 'IN_PROGRESS': 'primary', 'RESOLVED': 'success', 'CANCELED': 'danger'}
        badge_class = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge badge-{}">{}</span>', badge_class, obj.get_status_display())
    status_badge.short_description = 'Status Visual'

    def priority_badge(self, obj):
        colors = {'HIGH': 'danger', 'MEDIUM': 'warning', 'LOW': 'info'}
        badge_class = colors.get(obj.priority, 'secondary')
        return format_html('<span class="badge badge-{}">{}</span>', badge_class, obj.get_priority_display())
    priority_badge.short_description = 'Urgência'

    def photo_view(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 250px; border-radius: 10px; border: 1px solid #ccc;" />', obj.photo.url)
        return "Sem foto enviada"

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'total_votes_display', 'created_at')
    
    def total_votes_display(self, obj):
        return obj.total_votes()
    total_votes_display.short_description = 'Votos'