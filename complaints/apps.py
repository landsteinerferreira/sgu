from django.apps import AppConfig

class ComplaintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'complaints'
    verbose_name = 'Solicitações'

    def ready(self):
        import complaints.signals