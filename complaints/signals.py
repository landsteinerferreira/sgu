from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def enviar_email_status(instance):
    try:
        # Assunto do e-mail
        subject = f'Atualização: Sua solicitação #{instance.pk} mudou de status'
        
        # Contexto para o template HTML
        context = {
            'usuario': instance.user.get_full_name() or instance.user.username,
            'titulo': instance.title,
            'status': instance.get_status_display(),
            'link': f'https://solicitacidadao.duckdns.org/complaints/{instance.pk}/'
        }

        # 1. Renderiza o HTML (Certifique-se que o arquivo existe em templates/emails/...)
        html_message = render_to_string('email/status_update.html', context)
        plain_message = strip_tags(html_message)

        # 2. Envia o e-mail
        send_mail(
            subject,
            plain_message,
            'Solicita Cidadão <noreply@solicitacidadao.duckdns.org>',
            [instance.user.email],
            html_message=html_message,
            fail_silently=True, 
        )
        print(f"SUCESSO: E-mail enviado para {instance.user.email}")
        
    except Exception as e:
        print(f"ERRO AO ENVIAR E-MAIL: {e}")

@receiver(pre_save, sender='complaints.Complaints')
def notificar_mudanca_status(sender, instance, **kwargs):
    # Importação dentro da função para evitar ImportError circular
    from .models import Complaints
    
    if instance.pk:
        try:
            obj_antigo = Complaints.objects.get(pk=instance.pk)
            if obj_antigo.status != instance.status:
                print(f"DEBUG: O status mudou de {obj_antigo.status} para {instance.status}!")
                enviar_email_status(instance)
        except Complaints.DoesNotExist:
            pass