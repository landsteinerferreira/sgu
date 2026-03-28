from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Profile  # Certifique-se de que o Profile está no seu models.py

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


# --- VIEWS ---

def register_view(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = RegisterForm()

    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('complaints_list')
    else:
        login_form = AuthenticationForm()

    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('home')