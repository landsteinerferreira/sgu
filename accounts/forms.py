from django import foreign
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(label="Telefone/WhatsApp", max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # O signal já criou o profile, agora só atualizamos o telefone
            profile = Profile.objects.get(user=user)
            profile.phone = self.cleaned_data.get('phone')
            profile.save()
        return user