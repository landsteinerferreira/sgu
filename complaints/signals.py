import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# --- FUNÇÃO DE E-MAIL (MANTIDA) ---
def enviar_email_status(instance):
    try:
        subject = f'Atualização: Sua solicitação #{instance.pk} mudou de status'
        context = {
            'usuario': instance.user.get_full_name() or instance.user.username,
            'titulo': instance.title,
            'status': instance.get_status_display(),
            'link': f'https://solicitacidadao.duckdns.org/complaints/{instance.pk}/'
        }
        html_message = render_to_string('email/status_update.html', context)
        plain_message = strip_tags(html_message)

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

# --- SINAL: NOTIFICAÇÃO DE STATUS (MANTIDO) ---
@receiver(pre_save, sender='complaints.Complaints')
def notificar_mudanca_status(sender, instance, **kwargs):
    from .models import Complaints
    if instance.pk:
        try:
            obj_antigo = Complaints.objects.get(pk=instance.pk)
            if obj_antigo.status != instance.status:
                enviar_email_status(instance)
        except Complaints.DoesNotExist:
            pass

# --- SINAL: LIMPEZA AO DELETAR REGISTRO ---
@receiver(post_delete, sender='complaints.Complaints')
def delete_file_on_delete(sender, instance, **kwargs):
    """Apaga o arquivo físico do HD quando o registro é deletado no banco."""
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
            print(f"LIMPEZA: Arquivo {instance.photo.name} removido do servidor.")

# --- SINAL: LIMPEZA AO ATUALIZAR FOTO ---
@receiver(pre_save, sender='complaints.Complaints')
def delete_file_on_change(sender, instance, **kwargs):
    """Apaga a foto antiga se o usuário subir uma nova para o mesmo registro."""
    from .models import Complaints
    if not instance.pk:
        return False

    try:
        old_file = Complaints.objects.get(pk=instance.pk).photo
    except Complaints.DoesNotExist:
        return False

    new_file = instance.photo
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            print(f"LIMPEZA: Foto antiga substituída e removida.")