from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
)
from .models import Complaints, Suggestion
from complaints.forms import ComplaintsModelForm

# --- MIXINS DE REUTILIZAÇÃO ---

class OwnerOnlyMixin(UserPassesTestMixin):
    """Garante que apenas o dono do registro possa editá-lo ou deletá-lo."""
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

# --- SOLICITAÇÕES (COMPLAINTS) ---

class ComplaintsListView(ListView):
    model = Complaints
    template_name = 'complaints.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        # select_related('category') evita múltiplas consultas ao banco para o nome da categoria
        queryset = Complaints.objects.select_related('category').filter(
            status__in=['OPEN', 'IN_PROGRESS']
        ).order_by('-created_at')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

@method_decorator(login_required(login_url='login'), name='dispatch')
class MyComplaintsListView(ComplaintsListView):
    """Reutiliza a lógica de busca, mas filtra apenas as do usuário."""
    def get_queryset(self):
        queryset = Complaints.objects.select_related('category').filter(
            user=self.request.user
        ).order_by('-created_at')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

class ComplaintsDetailView(DetailView):
    model = Complaints
    template_name = 'complaints_detail.html'
    # select_related aqui garante que os detalhes da categoria carreguem rápido
    queryset = Complaints.objects.select_related('category', 'user')

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewComplaintsCreateView(CreateView):
    model = Complaints
    form_class = ComplaintsModelForm
    template_name = 'new_complaints.html'
    success_url = reverse_lazy('complaints_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # Coleta geolocalização do POST (via JS no frontend)
        lat = self.request.POST.get('latitude')
        lon = self.request.POST.get('longitude')
        
        if lat and lon:
            form.instance.latitude = lat
            form.instance.longitude = lon
            form.instance.location = f"{lat},{lon}"
            
        messages.success(self.request, "Solicitação enviada com sucesso!")
        return super().form_valid(form)

class ComplaintsUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Complaints
    form_class = ComplaintsModelForm
    template_name = 'complaints_update.html'
    raise_exception = True 

    def get_success_url(self):
        return reverse_lazy('complaints_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Regra de negócio: Finalizadas são imutáveis para o cidadão
        if obj.status not in ['OPEN', 'IN_PROGRESS']:
            messages.error(request, "Solicitações finalizadas não podem ser editadas.")
            return redirect('complaints_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

class ComplaintsDeleteView(LoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = Complaints
    template_name = 'complaints_delete.html'
    success_url = reverse_lazy('complaints_list')

# --- DASHBOARDS E SUGESTÕES ---

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_complaints = Complaints.objects.filter(user=self.request.user)
        
        context.update({
            'total_complaints': Complaints.objects.count(),
            'my_complaints_count': user_complaints.count(),
            'categories_chart': Complaints.objects.values('category__name').annotate(total=Count('id')).order_by('-total')[:5],
            'sectors_chart': Complaints.objects.values('sector').annotate(total=Count('id')).order_by('-total')[:5],
        })
        return context

class SuggestionView(LoginRequiredMixin, CreateView):
    model = Suggestion
    template_name = 'suggestions.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('suggestions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ordena pelas mais votadas primeiro
        context['suggestions'] = Suggestion.objects.annotate(num_votes=Count('votes')).order_by('-num_votes')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def vote_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if suggestion.votes.filter(id=request.user.id).exists():
        suggestion.votes.remove(request.user)
    else:
        suggestion.votes.add(request.user)
    return redirect('suggestions')

# --- PÁGINAS PÚBLICAS / ADMIN ---

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_complaints': Complaints.objects.count(),
            'resolved_complaints': Complaints.objects.filter(status='RESOLVED').count(),
            'top_sectors': Complaints.objects.values('sector').annotate(total=Count('id')).order_by('-total')[:3],
        })
        return context

class AdminDashboardStatsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard_stats.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Agrupando consultas de contagem para performance
        stats = Complaints.objects.aggregate(
            total=Count('id'),
            open=Count('id', filter=Q(status='OPEN')),
            progress=Count('id', filter=Q(status='IN_PROGRESS')),
            resolved=Count('id', filter=Q(status='RESOLVED'))
        )
        
        context.update({
            'title': "Painel de Indicadores",
            'total_complaints': stats['total'],
            'open_complaints': stats['open'],
            'in_progress': stats['progress'],
            'resolved': stats['resolved'],
            # Dados geográficos para os pinos do Leaflet (Incluindo ID para o popup)
            'map_points': Complaints.objects.exclude(latitude__isnull=True).values(
                'id', 'latitude', 'longitude', 'title', 'category__name', 'status'
            ),
            # Ranking de Setores para a Tabela
            'all_sector_stats': Complaints.objects.values('sector').annotate(
                total=Count('id'),
                abertas=Count('id', filter=Q(status='OPEN')),
                resolvidas=Count('id', filter=Q(status='RESOLVED'))
            ).order_by('-total')
        })
        return context