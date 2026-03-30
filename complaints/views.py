from django.db.models import Q
from django.db.models import Count  # Adicionado
from .models import Complaints, Suggestion  # Adicionado
from complaints.forms import ComplaintsModelForm
from django.views.generic import TemplateView, ListView, UpdateView  # Adicionado
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Adicionado
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404


# Feed de todos
class ComplaintsListView(ListView):
    model = Complaints
    template_name = 'complaints.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        # Filtro base
        queryset = Complaints.objects.filter(
            status__in=['OPEN', 'IN_PROGRESS']
        ).order_by('-created_at')

        # Lógica de busca
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        return queryset


# Minhas Solicitações
@method_decorator(login_required(login_url='login'), name='dispatch')
class MyComplaintsListView(ComplaintsListView):
    # Opcional: Se quiser um template diferente para as "Minhas"
    # template_name = 'my_complaints.html' 

    def get_queryset(self):
        # 1. Começamos do zero (todos os registros do usuário logado)
        # Diferente da classe pai, aqui NÃO filtramos por status fixo
        queryset = Complaints.objects.filter(user=self.request.user).order_by('-created_at')

        # 2. Reutilizamos a lógica de busca por texto (Barra de Pesquisa)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset


class ComplaintsDetailView(DetailView):
    model = Complaints
    template_name = 'complaints_detail.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class NewComplaintsCreateView(CreateView):
    model = Complaints
    form_class = ComplaintsModelForm
    template_name = 'new_complaints.html'
    success_url = '/complaints/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ComplaintsUpdateView(UpdateView):
    model = Complaints  # Modelo
    form_class = ComplaintsModelForm
    template_name = 'complaints_update.html'

    # página 403 personalizada
    raise_exception = True 

    # Teste de segurança
    def test_func(self):
        complaint = self.get_object()
        return self.request.user == complaint.user  # Retorna True se for o dono

    def get_success_url(self):
        return reverse_lazy('complaints_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Se tentar editar algo que não está aberto ou em progresso, bloqueia
        if obj.status not in ['OPEN', 'IN_PROGRESS']:
            messages.error(request, "Solicitações finalizadas não podem ser editadas.")
            return redirect('complaints_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ComplaintsDeleteView(DeleteView):
    model = Complaints  # Modelo
    template_name = 'complaints_delete.html'
    success_url = '/complaints/'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Estatísticas Gerais
        context['total_complaints'] = Complaints.objects.count()
        context['my_complaints_count'] = Complaints.objects.filter(user=self.request.user).count()

        # 2. Reclamações por Categoria (Top 5)
        # Isso retorna algo como: [{'category__name': 'Buraco', 'total': 10}, ...]
        context['categories_chart'] = Complaints.objects.values('category__name').annotate(
            total=Count('id')
        ).order_by('-total')[:5]

        # 3. Reclamações por Setor/Bairro
        context['sectors_chart'] = Complaints.objects.values('sector').annotate(
            total=Count('id')
        ).order_by('-total')[:5]

        return context


#  Sugestões
class SuggestionView(LoginRequiredMixin, CreateView):
    model = Suggestion
    template_name = 'suggestions.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('suggestions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = Suggestion.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# View rápida para votar
@login_required
def vote_suggestion(request, pk):

    suggestion = get_object_or_404(Suggestion, pk=pk)
    if suggestion.votes.filter(id=request.user.id).exists():
        suggestion.votes.remove(request.user)
    else:
        suggestion.votes.add(request.user)
    return redirect('suggestions')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Chama a implementação base primeiro para pegar o contexto padrão
        context = super().get_context_data(**kwargs)
        
        # Adiciona dados dinâmicos para a Landing Page
        context['total_complaints'] = Complaints.objects.count()
        context['resolved_complaints'] = Complaints.objects.filter(status='resolvido').count()
        
        # Opcional: Pegar os 3 bairros mais ativos para mostrar na Home
        context['top_sectors'] = Complaints.objects.values('sector').annotate(
            total=Count('id')
        ).order_by('-total')[:3]
        
        return context

#  Dashboard dentro do Admin do Django
class AdminDashboardStatsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard_stats.html'

    # Garante que apenas Staff (equipe) acesse essa view
    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dados para os Cards
        context['total_complaints'] = Complaints.objects.count()
        context['open_complaints'] = Complaints.objects.filter(status='OPEN').count()
        context['in_progress'] = Complaints.objects.filter(status='IN_PROGRESS').count()
        context['resolved'] = Complaints.objects.filter(status='RESOLVED').count()
        
        # Dados para Gráficos ou Listas (ex: Top 5 bairros com problemas)
        context['sector_stats'] = Complaints.objects.values('sector').annotate(
            total=Count('id')
        ).order_by('-total')[:5]

        # Título da página para o Jazzmin
        context['title'] = "Painel de Indicadores"
        return context
