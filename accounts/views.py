from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# --- FORMULÁRIO PERSONALIZADO DE REGISTRO ---
class RegisterForm(UserCreationForm):
    # O Django usa 'first_name' internamente, vamos usá-lo para guardar o Nome Completo
    first_name = forms.CharField(
        label="Nome Completo",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'})
    )
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Ex: seuemail@email.com'})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")  # Define a ordem dos campos no HTML


# --- VIEWS ---

def register_view(request):
    if request.method == "POST":
        # Usamos o formulário personalizado criado acima
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = RegisterForm()

    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == "POST":
        # Passamos o request e os dados do POST para o formulário de autenticação
        login_form = AuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            # O cleaned_data garante que os dados estão limpos e seguros
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('complaints_list')
        # Se não for válido, o formulário já carrega os erros para o template
    else:
        login_form = AuthenticationForm()

    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('home')
