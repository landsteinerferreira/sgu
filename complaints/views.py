import csv
import json
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
)
from .models import Complaints, Suggestion, PushSubscription, Category, SECTOR_CHOICES, STATUS_CHOICES
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
    template_name = 'complaints/complaints.html'
    context_object_name = 'complaints'
    paginate_by = 10

    def get_queryset(self):
        queryset = Complaints.objects.select_related('category').filter(
            status__in=['OPEN', 'IN_PROGRESS']
        ).order_by('-created_at')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        return context

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

        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))

        return queryset

class ComplaintsDetailView(DetailView):
    model = Complaints
    template_name = 'complaints/complaints_detail.html'
    # select_related aqui garante que os detalhes da categoria carreguem rápido
    queryset = Complaints.objects.select_related('category', 'user')

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewComplaintsCreateView(CreateView):
    model = Complaints
    form_class = ComplaintsModelForm
    template_name = 'complaints/new_complaints.html'
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
    template_name = 'complaints/complaints_update.html'
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
    template_name = 'complaints/complaints_delete.html'
    success_url = reverse_lazy('complaints_list')

# --- DASHBOARDS E SUGESTÕES ---

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'complaints/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_complaints = Complaints.objects.filter(user=self.request.user)
        
        context.update({
            'total_complaints': Complaints.objects.count(),
            'my_complaints_count': user_complaints.count(),
            'categories_chart': Complaints.objects.values('category__name').annotate(total=Count('id')).order_by('-total')[:5],
            'sectors_chart': [
                {**item, 'sector': dict(SECTOR_CHOICES).get(item['sector'], item['sector'])}
                for item in Complaints.objects.values('sector').annotate(total=Count('id')).order_by('-total')[:5]
            ],
        })
        return context

class SuggestionView(LoginRequiredMixin, CreateView):
    model = Suggestion
    template_name = 'complaints/suggestions.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('suggestions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.request.GET.get('order', 'votes')
        base_qs = Suggestion.objects.annotate(num_votes=Count('votes'))
        if order == 'recent':
            context['suggestions'] = base_qs.order_by('-created_at')
        else:
            context['suggestions'] = base_qs.order_by('-num_votes')
        context['current_order'] = order
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Sugestão enviada com sucesso!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('order', '') and reverse_lazy('suggestions') + f'?order={self.request.GET.get("order")}' or reverse_lazy('suggestions')

class VoteSuggestionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        suggestion = get_object_or_404(Suggestion, pk=pk)
        if suggestion.votes.filter(id=request.user.id).exists():
            suggestion.votes.remove(request.user)
        else:
            suggestion.votes.add(request.user)
        order = request.GET.get('order', '')
        if order:
            return redirect(f'{reverse_lazy("suggestions")}?order={order}')
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
            'live_feed': Complaints.objects.select_related('category', 'user').exclude(
                status='OPEN'
            ).order_by('-updated_at')[:5],
            'map_points': Complaints.objects.filter(
                status__in=['OPEN', 'IN_PROGRESS']
            ).exclude(
                latitude__isnull=True
            ).values(
                'id', 'latitude', 'longitude', 'title', 'category__name', 'status', 'sector'
            )[:100],
        })
        return context


class LiveFeedJsonView(TemplateView):
    template_name = 'complaints/partials/live_feed_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['live_feed'] = Complaints.objects.select_related('category', 'user').exclude(
            status='OPEN'
        ).order_by('-updated_at')[:5]
        return context

class AdminDashboardStatsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'complaints/admin/dashboard_stats.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        status_filter = self.request.GET.get('status', '')
        valid_statuses = dict(STATUS_CHOICES)
        if status_filter not in valid_statuses:
            status_filter = ''
        
        base_qs = Complaints.objects.all()
        map_qs = Complaints.objects.exclude(latitude__isnull=True)
        sector_qs = Complaints.objects.all()
        
        if status_filter:
            base_qs = base_qs.filter(status=status_filter)
            map_qs = map_qs.filter(status=status_filter)
            sector_qs = sector_qs.filter(status=status_filter)
        
        stats = base_qs.aggregate(
            total=Count('id'),
            open=Count('id', filter=Q(status='OPEN')),
            progress=Count('id', filter=Q(status='IN_PROGRESS')),
            resolved=Count('id', filter=Q(status='RESOLVED'))
        )
        
        context.update({
            'title': "Painel de Indicadores",
            'current_status': status_filter,
            'total_complaints': stats['total'],
            'open_complaints': stats['open'],
            'in_progress': stats['progress'],
            'resolved': stats['resolved'],
            # Dados geográficos para os pinos do Leaflet (Incluindo ID para o popup)
            'map_points': map_qs.values(
                'id', 'latitude', 'longitude', 'title', 'category__name', 'status'
            ),
            # Ranking de Setores para a Tabela
            'all_sector_stats': [
                {**item, 'sector': dict(SECTOR_CHOICES).get(item['sector'], item['sector'])}
                for item in sector_qs.values('sector').annotate(
                    total=Count('id'),
                    abertas=Count('id', filter=Q(status='OPEN')),
                    resolvidas=Count('id', filter=Q(status='RESOLVED'))
                ).order_by('-total')
            ],
        })
        return context


@method_decorator([login_required, csrf_exempt], name='dispatch')
class SubscribePushView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            PushSubscription.objects.update_or_create(
                user=request.user,
                endpoint=data.get('endpoint'),
                defaults={
                    'auth_key': data['keys']['auth'],
                    'p256dh_key': data['keys']['p256dh'],
                }
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@method_decorator([login_required, csrf_exempt], name='dispatch')
class UnsubscribePushView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            PushSubscription.objects.filter(
                user=request.user,
                endpoint=data.get('endpoint')
            ).delete()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ExportComplaintsCSVView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status', '')
        valid_statuses = dict(STATUS_CHOICES)
        if status_filter not in valid_statuses:
            status_filter = ''

        qs = Complaints.objects.select_related('category', 'user').order_by('-created_at')
        if status_filter:
            qs = qs.filter(status=status_filter)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="solicitacoes.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'ID', 'Título', 'Descrição', 'Categoria', 'Status', 'Prioridade',
            'Endereço', 'Bairro', 'Cidade', 'Latitude', 'Longitude',
            'Usuário', 'Resposta', 'Criado em', 'Atualizado em'
        ])

        for c in qs:
            writer.writerow([
                c.id, c.title, c.description, c.category.name,
                c.get_status_display(), c.get_priority_display(),
                c.address, c.get_sector_display(), c.city,
                str(c.latitude).replace('.', ','),
                str(c.longitude).replace('.', ','),
                c.user.username,
                c.feedback_agency or '',
                c.created_at.strftime('%d/%m/%Y %H:%M'),
                c.updated_at.strftime('%d/%m/%Y %H:%M'),
            ])

        return response