from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register_view, login_view, logout_view
from complaints.views import (
    ComplaintsListView, ComplaintsDetailView, NewComplaintsCreateView, 
    ComplaintsUpdateView, ComplaintsDeleteView, MyComplaintsListView, 
    DashboardView, SuggestionView, vote_suggestion, HomeView, AdminDashboardStatsView
)

urlpatterns = [
    # 1. PWA e ADMIN (Devem vir primeiro para o manifesto ser encontrado)
    path('', include('pwa.urls')), 
    path('admin/', admin.site.urls),
    path('admin/dashboard-stats/', AdminDashboardStatsView.as_view(), name='admin_stats'),

    # 2. PÁGINA INICIAL
    path('', HomeView.as_view(), name='home'),

    # 3. CONTAS
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # 4. SOLICITAÇÕES (COMPLAINTS)
    path('complaints/', ComplaintsListView.as_view(), name='complaints_list'),
    path('my_complaints/', MyComplaintsListView.as_view(), name='my_complaints'),
    path('new_complaints/', NewComplaintsCreateView.as_view(), name='new_complaints'),
    path('complaints/<int:pk>/', ComplaintsDetailView.as_view(), name='complaints_detail'),
    path('complaints/<int:pk>/update/', ComplaintsUpdateView.as_view(), name='complaints_update'),
    path('complaints/<int:pk>/delete/', ComplaintsDeleteView.as_view(), name='complaints_delete'),
    
    # 5. DASHBOARD E SUGESTÕES
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('sugestoes/', SuggestionView.as_view(), name='suggestions'),
    path('sugestoes/votar/<int:pk>/', vote_suggestion, name='vote_suggestion'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Garante que estáticos funcionem em qualquer ambiente
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)