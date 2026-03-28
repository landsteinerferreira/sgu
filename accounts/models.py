from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Relaciona o perfil a um usuário existente
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # O campo de contato (telefone/whatsapp)
    phone = models.CharField(max_length=20, verbose_name="Telefone/WhatsApp", blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"

from django.db.models.signals import post_save
from django.dispatch import receiver


# Este decorator diz que a função abaixo deve rodar sempre que um User for salvo
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()