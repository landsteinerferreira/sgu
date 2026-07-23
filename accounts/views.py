from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Profile

# --- FORMULÁRIO PERSONALIZADO DE REGISTRO ---
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome Completo",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Ex: seuemail@email.com', 'class': 'form-control'})
    )
    # NOVO CAMPO DE TELEFONE
    phone = forms.CharField(
        label="Telefone / WhatsApp",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "phone")

    # Lógica para salvar o Telefone no Profile
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # O Signal já criou o Profile, agora buscamos e atualizamos o telefone
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone')
            profile.save()
        return user


# --- VIEWS (Class-Based) ---

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = context.get('form')
        return context


class EmailOrUsernameLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário ou E-mail",
        widget=forms.TextInput(attrs={'placeholder': 'Usuário ou e-mail', 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'class': 'form-control'})
    )

    def clean_username(self):
        value = self.cleaned_data['username']
        if '@' in value:
            try:
                user = User.objects.get(email=value)
                return user.username
            except User.DoesNotExist:
                raise forms.ValidationError("E-mail não encontrado.")
        return value


class UserLoginView(AuthLoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailOrUsernameLoginForm
    next_page = reverse_lazy('complaints_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.get_form()
        return context


class UserLogoutView(AuthLogoutView):
    next_page = reverse_lazy('home')