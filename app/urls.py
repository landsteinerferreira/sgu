from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import RegisterView, UserLoginView, UserLogoutView
from complaints.views import (
    ComplaintsListView, ComplaintsDetailView, NewComplaintsCreateView, 
    ComplaintsUpdateView, ComplaintsDeleteView, MyComplaintsListView, 
    DashboardView, SuggestionView, VoteSuggestionView, HomeView, 
    AdminDashboardStatsView, LiveFeedJsonView, ExportComplaintsCSVView,
    SubscribePushView, UnsubscribePushView
)

urlpatterns = [
    # 1. PWA (O PWA precisa da raiz para registrar o Service Worker corretamente)
    path('', include('pwa.urls')), 

    # 2. ADMIN E DASHBOARD CUSTOMIZADA
    # Colocamos a dashboard ANTES do admin padrão para garantir a precedência da rota
    path('admin/dashboard-stats/', AdminDashboardStatsView.as_view(), name='admin_dashboard_stats'),
    path('admin/dashboard-stats/exportar-csv/', ExportComplaintsCSVView.as_view(), name='export_complaints_csv'),
    path('admin/', admin.site.urls),

    # 3. PÁGINA INICIAL (HOME)
    path('', HomeView.as_view(), name='home'),

    # 4. CONTAS / AUTENTICAÇÃO
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.txt',
        html_email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete'),
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),

    # 5. API TEMPO REAL
    path('live-feed/', LiveFeedJsonView.as_view(), name='live_feed'),

    # 6. API NOTIFICAÇÕES PUSH
    path('push/subscribe/', SubscribePushView.as_view(), name='subscribe_push'),
    path('push/unsubscribe/', UnsubscribePushView.as_view(), name='unsubscribe_push'),

    # 7. SOLICITAÇÕES (COMPLAINTS)
    path('complaints/', ComplaintsListView.as_view(), name='complaints_list'),
    path('my_complaints/', MyComplaintsListView.as_view(), name='my_complaints'),
    path('new_complaints/', NewComplaintsCreateView.as_view(), name='new_complaints'),
    path('complaints/<int:pk>/', ComplaintsDetailView.as_view(), name='complaints_detail'),
    path('complaints/<int:pk>/update/', ComplaintsUpdateView.as_view(), name='complaints_update'),
    path('complaints/<int:pk>/delete/', ComplaintsDeleteView.as_view(), name='complaints_delete'),
    
    # 8. DASHBOARD DO USUÁRIO E SUGESTÕES
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('sugestoes/', SuggestionView.as_view(), name='suggestions'),
    path('sugestoes/votar/<int:pk>/', VoteSuggestionView.as_view(), name='vote_suggestion'),

]

# 9. ARQUIVOS DE MÍDIA E ESTÁTICOS
# Adicionando de forma robusta para desenvolvimento e produção
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Em produção, o WhiteNoise ou Nginx cuida disso, mas mantemos o mapeamento de Media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)