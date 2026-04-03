import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['129.148.28.59', 'solicitacidadao.duckdns.org', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'complaints',
    'accounts',
    'location_field.apps.DefaultConfig',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        #  Usando postgresql
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'complaints', #  Nome do banco
        'USER': 'postgres', #  Usuario
        'PASSWORD': 'Lands@a627ha', #  Senha
        'HOST': 'localhost', #  Local so servidor
        'PORT': '5432', # Porta
        #  Usando o sqlite3
        #'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


JAZZMIN_SETTINGS = {
    
    # Título da aba do navegador
    "site_title": "Solicita Cidadão Admin",
    
    # Título no painel (aquele que aparece no login)
    "site_header": "Solicita Cidadão",

    "site_brand": "",

    # Logo no topo do menu lateral (após logar) - tamanho menor
    "site_logo": "images/logo_solicita_cidadao.png",

    "site_logo_classes": "img-fluid",

    # Classe CSS para a logo (ajuda no dimensionamento)
    "site_logo_classes": "img-fluid",

    # Se você quer que a logo apareça em tamanho maior no topo:
    "site_logo_style": "max-height: 50px;", # Ajuste a altura conforme necessário
    
    # Boas-vindas na tela de login
    "welcome_sign": "Bem-vindo ao Painel de Gestão de Trindade",
    
    # Copyright no rodapé
    "copyright": "Solicita Cidadão Ltda",

    # Menu de busca global no topo
    "search_model": "complaints.Complaints",

    # Injeta um CSS customizado para corrigir o topo e o perfil
    "custom_css": "css/custom_admin.css",

    # --- Configuração do Menu Lateral ---
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "complaints.Complaints"},
    ],
    
    # Ícones para os modelos (usando Font Awesome)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "complaints.Complaints": "fas fa-exclamation-triangle",
        "complaints.Category": "fas fa-list",
        "complaints.Suggestion": "fas fa-lightbulb",
    },
    
    # Mostrar o menu lateral expandido por padrão
    "show_sidebar": True,
    "navigation_expanded": True,

    "custom_links": {
        "complaints": [{
            "name": "Ver Estatísticas Reais", 
            "url": "/admin/dashboard-stats/", 
            "icon": "fas fa-chart-pie",
        }],
    },
    # Isso permite que você mude a página inicial do admin
    "changeform_format": "horizontal_tabs",

    
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary", # Usa o azul padrão
    "accent": "accent-primary",
    "navbar": "navbar-dark", # Navbar escura para contraste
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary", # Menu lateral escuro com destaque azul
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cerulean",
    "theme_mode": "auto",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}


# Configurações de envio de e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # Use senha de app do Google
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')


# Mapas interativos
LOCATION_FIELD = {
    'map_widgets': (
        'location_field.widgets.LeafletWidget',
    ),
    'provider': 'openstreetmap',
}


# Configurações do PWA
PWA_APP_NAME = 'Solicita Cidadão'
PWA_APP_DESCRIPTION = "Zeladoria Urbana de Trindade"
PWA_APP_THEME_COLOR = '#0096C7'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'

# O segredo para o PWA ativar no navegador é o Service Worker
# Esta linha aponta para o arquivo que o collectstatic gera
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')

PWA_APP_ICONS = [
    {
        'src': '/static/images/icon-160x160.png',
        'sizes': '160x160',
        'type': 'image/png'
    },
    {
        'src': '/static/images/icon-512x512.png',
        'sizes': '512x512',
        'type': 'image/png'
    }
]

# Configurações para iOS
PWA_APP_ICONS_APPLE = PWA_APP_ICONS
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'pt-BR'