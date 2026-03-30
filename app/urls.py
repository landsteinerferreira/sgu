from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register_view, login_view, logout_view
from complaints.views import ComplaintsListView, ComplaintsDetailView, NewComplaintsCreateView, ComplaintsUpdateView, ComplaintsDeleteView, MyComplaintsListView, DashboardView, SuggestionView, vote_suggestion, HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    #path('', ComplaintsListView.as_view(), name='complaints_list'),
    path('admin/', admin.site.urls),
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('complaints/', ComplaintsListView.as_view(), name='complaints_list'),
    path('my_complaints/', MyComplaintsListView.as_view(), name='my_complaints'),
    path('new_complaints/', NewComplaintsCreateView.as_view(), name='new_complaints'),
    path('complaints/<int:pk>/', ComplaintsDetailView.as_view(), name='complaints_detail'),
    path('complaints/<int:pk>/update/', ComplaintsUpdateView.as_view(), name='complaints_update'),
    path('complaints/<int:pk>/delete/', ComplaintsDeleteView.as_view(), name='complaints_delete'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('sugestoes/', SuggestionView.as_view(), name='suggestions'),
    path('sugestoes/votar/<int:pk>/', vote_suggestion, name='vote_suggestion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
