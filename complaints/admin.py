from django.contrib import admin
from django.utils.html import format_html
from complaints.models import Category, Complaints, Suggestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    # CORREÇÃO: Adicionei 'status' e 'priority' aqui para o list_editable funcionar
    list_display = (
        'protocolo', 
        'title', 
        'sector', 
        'status',           # Campo original (necessário para o editable)
        'status_badge',     # Versão visual com badge
        'priority',         # Campo original (necessário para o editable)
        'priority_badge',   # Versão visual com badge
        'user', 
        'created_at'
    )
    
    # Agora o Django vai permitir editar sem reclamar
    list_editable = ('status', 'priority')
    
    list_filter = ('status', 'priority', 'sector', 'category', 'created_at')
    search_fields = ('title', 'description', 'address', 'user__username')
    list_per_page = 20

    fieldsets = (
        ('Dados do Cidadão', {
            'fields': (('user', 'category'), 'title', 'description', 'photo_view'),
        }),
        ('Localização', {
            'fields': ('sector', 'address'),
        }),
        ('Ação da Prefeitura', {
            'fields': ('priority', 'status', 'feedback_agency'),
        }),
    )

    readonly_fields = ('user', 'title', 'description', 'category', 'sector', 'address', 'photo_view', 'created_at')

    # --- Funções Auxiliares ---
    def protocolo(self, obj):
        return format_html("<b>#{}</b>", obj.id)
    protocolo.short_description = 'Prot.'

    def status_badge(self, obj):
        colors = {'OPEN': 'warning', 'IN_PROGRESS': 'primary', 'RESOLVED': 'success', 'CANCELED': 'danger'}
        badge_class = colors.get(obj.status, 'secondary')
        return format_html('<span class="badge badge-{}">{}</span>', badge_class, obj.get_status_display())
    status_badge.short_description = 'Visual'

    def priority_badge(self, obj):
        colors = {'HIGH': 'danger', 'MEDIUM': 'warning', 'LOW': 'info'}
        badge_class = colors.get(obj.priority, 'secondary')
        return format_html('<span class="badge badge-{}">{}</span>', badge_class, obj.get_priority_display())
    priority_badge.short_description = 'Urgência'

    def photo_view(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.photo.url)
        return "Sem foto"

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'total_votes', 'created_at')
