from django.db.models import Count  # Adicionado
from .models import Complaints, Suggestion  # Adicionado
from complaints.forms import ComplaintsModelForm
from django.views.generic import TemplateView  # Adicionado
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # Adicionado
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404


# Feed de todos
class ComplaintsListView(ListView):
    model = Complaints
    template_name = 'complaints.html'
    context_object_name = 'complaints'
    paginate_by = 6

    def get_queryset(self):
        complaints = super().get_queryset().order_by('-id')

        search = self.request.GET.get('search')
        if search:
            complaints = complaints.filter(title__icontains=search)
        return complaints


# Minhas Solicitações
@method_decorator(login_required(login_url='login'), name='dispatch')
class MyComplaintsListView(ComplaintsListView):
    def get_queryset(self):
        # Reutiliza a lógica de busca, mas filtra apenas pelo usuário logado
        return super().get_queryset().filter(user=self.request.user)


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

    def get_success_url(self):
        return reverse_lazy('complaints_detail', kwargs={'pk': self.object.pk})


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
