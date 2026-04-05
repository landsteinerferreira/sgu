from django.contrib import admin
from django.utils.html import format_html
from complaints.models import Category, Complaints, Suggestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('id_protocolo', 'title', 'sector', 'status_badge', 'priority_badge', 'user', 'created_at')
    list_editable = ('sector',)
    list_filter = ('status', 'priority', 'sector', 'category', 'created_at')
    search_fields = ('title', 'description', 'address', 'user__username')
    list_per_page = 20

    fieldsets = (
        ('Informações da Ocorrência', {
            'fields': (('user', 'category'), 'title', 'description', 'photo_view'),
        }),
        ('Localização Geográfica', {
            'fields': ('sector', 'address', 'map_view'),
        }),
        ('Gestão e Resposta da Prefeitura', {
            'fields': ('priority', 'status', 'feedback_agency'),
        }),
    )

    readonly_fields = ('user', 'category', 'title', 'description', 'photo_view', 'created_at', 'map_view')

    class Media:
        css = {
            'all': (
                'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
                'https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css',
            )
        }
        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js',
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['jazzmin_custom_css'] = """
            .field-priority, .field-status {
                display: block !important; float: left !important; width: 50% !important;
                padding: 20px !important; box-sizing: border-box !important;
                background: #f8f9fa !important; border: 1px solid #eee !important;
            }
            .field-feedback_agency { clear: both !important; width: 100% !important; padding: 20px !important; border-top: 2px solid #007bff !important; }
            .field-feedback_agency textarea { width: 100% !important; min-height: 200px !important; }
            .form-group label { width: 100% !important; margin-bottom: 10px !important; font-weight: bold !important; }
            .form-horizontal .form-group { margin-left: 0 !important; margin-right: 0 !important; }
        """
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    # --- MÉTODOS VISUAIS ---
    def id_protocolo(self, obj):
        return format_html("<b>#{}</b>", obj.id)

    def status_badge(self, obj):
        map_status = {'OPEN': ('warning', 'Aberto'), 'IN_PROGRESS': ('primary', 'Atendimento'), 'RESOLVED': ('success', 'Resolvido')}
        color, label = map_status.get(obj.status, ('secondary', obj.status))
        return format_html('<span class="badge badge-{}">{}</span>', color, label)

    def priority_badge(self, obj):
        map_prio = {'HIGH': ('danger', 'Alta'), 'MEDIUM': ('warning', 'Média'), 'LOW': ('info', 'Baixa')}
        color, label = map_prio.get(obj.priority, ('secondary', 'N/A'))
        return format_html('<span class="badge badge-{}">{}</span>', color, label)

    def photo_view(self, obj):
        if obj.photo: return format_html('<img src="{}" style="max-height: 300px; border-radius: 8px;"/>', obj.photo.url)
        return "Sem foto."

    def map_view(self, obj):
        if not obj.latitude or not obj.longitude: return "GPS indisponível."
        
        # DEFINIÇÃO DE CORES (IDÊNTICAS AO DASHBOARD)
        # Usamos o Status para a cor do pino e a Prioridade para o texto, mantendo a coerência.
        color_map = {'OPEN': '#dc3545', 'IN_PROGRESS': '#ffc107', 'RESOLVED': '#28a745'}
        status_color = color_map.get(obj.status, '#6c757d')

        return format_html(
            '''
            <div style="width: 100%; border: 2px solid #333; border-radius: 8px; overflow: hidden;">
                <div id="map_canvas" style="height: 550px; width: 100%;"></div>
            </div>
            <script>
                window.addEventListener('load', function() {{
                    setTimeout(function() {{
                        var lat = parseFloat("{lat}");
                        var lon = parseFloat("{lon}");
                        if (isNaN(lat) || isNaN(lon)) return;

                        var map = L.map('map_canvas', {{fullscreenControl: true}}).setView([lat, lon], 17);
                        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
                        
                        // CÍRCULO COLORIDO (ESTILO DASHBOARD)
                        L.circleMarker([lat, lon], {{
                            radius: 12,
                            fillColor: "{color}",
                            color: "#fff",
                            weight: 3,
                            opacity: 1,
                            fillOpacity: 0.9
                        }}).addTo(map).bindPopup(`
                            <div style="min-width: 200px; font-family: sans-serif;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                    <small>#ID: {id}</small>
                                    <span style="font-size: 10px; font-weight: bold; color: #fff; background-color: {color}; padding: 2px 6px; border-radius: 4px;">{status}</span>
                                </div>
                                <h6 style="margin: 0; color: #007bff; font-weight: bold;">{title}</h6>
                                <p style="margin: 5px 0; font-size: 13px; color: #333;">{description}</p>
                            </div>
                        `).openPopup();

                        setTimeout(function() {{ map.invalidateSize(); }}, 500);
                    }}, 600);
                }});
            </script>
            ''',
            lat=obj.latitude,
            lon=obj.longitude,
            color=status_color,
            id=obj.id,
            title=obj.title,
            status=obj.get_status_display().upper(),
            description=obj.description if obj.description else ""
        )

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')