# Solicita Cidadão

Sistema de zeladoria urbana para a cidade de Trindade-GO. Plataforma onde cidadãos podem registrar solicitações sobre problemas urbanos (buracos, entulho, iluminação, etc.) e acompanhar o status até a resolução.

## Funcionalidades

- **Feed público** — lista de solicitações abertas com busca e filtro por categoria
- **Cadastro de solicitações** — com foto, geolocalização (GPS) e endereço
- **Acompanhamento em tempo real** — feed ao vivo de mudanças de status
- **Dashboard do cidadão** — estatísticas pessoais e rankings por categoria/bairro
- **Mural de Ideias** — sugestões da comunidade com sistema de votação
- **Painel admin** — mapa interativo com heatmap, KPIs, ranking por setor, exportação CSV
- **Notificações** — e-mail e push notification no navegador ao alterar status
- **PWA** — instalável como aplicativo no celular/desktop
- **Mapa público** — visualização geográfica das solicitações

## Stack

| Tecnologia | Versão |
|------------|--------|
| Python | 3.x |
| Django | 6.0.3 |
| Django Jazzmin | 3.0.4 |
| Django PWA | 2.0.1 |
| Django Location Field | 2.7.3 |
| PostgreSQL | — |
| WhiteNoise | 6.12.0 |
| Leaflet | 1.9.4 |
| pywebpush | 2.3.0 |

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone <repo-url>
cd sgu

# 2. Crie e ative o virtualenv
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env (veja .env.example)
# Preencha as variáveis de ambiente necessárias

# 5. Rode as migrações
python manage.py migrate

# 6. Crie um superusuário
python manage.py createsuperuser

# 7. Inicie o servidor
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

## Variáveis de Ambiente (.env)

```
SECRET_KEY=django-insecure-...
DEBUG=True
DB_NAME=complaints
DB_USER=postgres
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
VAPID_PUBLIC_KEY=...
VAPID_PRIVATE_KEY=...
```

## Estrutura do Projeto

```
sgu/
├── accounts/              # Autenticação e perfis de usuário
│   ├── models.py          # Profile (telefone)
│   ├── views.py           # register, login, logout
│   └── templates/
├── app/                   # Configuração do projeto
│   ├── settings.py
│   ├── urls.py
│   └── templates/         # base.html, home.html
├── complaints/            # Módulo principal
│   ├── models.py          # Complaints, Category, Suggestion, PushSubscription
│   ├── views.py           # CRUD, dashboards, export CSV, push
│   ├── admin.py           # Admin com mapa interativo
│   ├── signals.py         # E-mail e push notifications
│   └── templates/
├── static/                # CSS, JS, imagens
│   └── css/custom_admin.css
├── media/                 # Uploads (fotos)
├── staticfiles/           # Coletados para produção
├── manage.py
└── requirements.txt
```

## Admin

URL: `/admin/`

Recursos do painel administrativo:
- Dashboard com indicadores, mapa com heatmap e ranking de setores
- Filtros por status (Aberta, Em Andamento, Resolvida)
- Exportação de dados em CSV
- Visualização geográfica de cada solicitação

## Testes

```bash
python manage.py test
```

## Deploy

O sistema utiliza uWSGI + WhiteNoise para produção. Consulte `sgu_uwsgi.ini` para configuração do servidor.

## Licença

Projeto desenvolvido para obtenção de título de Especialista em Engenharia de Software — USP.

## Contato

Landsteiner Ferreira
Linkedin: https://br.linkedin.com/in/landsteiner-ferreira-da-silva-6ba49953
