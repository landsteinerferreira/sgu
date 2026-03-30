from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('OPEN', 'Aberta'),
    ('IN_PROGRESS', 'Em andamento'),
    ('RESOLVED', 'Resolvida'),
    ('CANCELED', 'Cancelada'),
]

PRIORITY_CHOICES = [
    ('LOW', 'Baixa'),
    ('MEDIUM', 'Média'),
    ('HIGH', 'Alta'),
]

SECTOR_CHOICES = [
    ("selecione_bairro", "Selecione o Bairro"),
    ("area_rural_de_trindade", "Área Rural de Trindade"),
    ("centro", "Centro"),
    ("chacara_parque_cristo_redentor", "Chácara Parque Cristo Redentor"),
    ("chacara_santa_luzia", "Chácara Santa Luzia"),
    ("conjunto_dona_iris", "Conjunto Dona Iris"),
    ("conjunto_dona_iris_ii", "Conjunto Dona Iris II"),
    ("conjunto_prive_elias", "Conjunto Privê Elias"),
    ("conjunto_sol_dourado", "Conjunto Sol Dourado"),
    ("estancias_aroeira", "Estâncias Aroeira"),
    ("guaruja_park", "Guarujá Park"),
    ("jardim_california", "Jardim Califórnia"),
    ("jardim_das_oliveiras", "Jardim das Oliveiras"),
    ("jardim_das_tamareiras", "Jardim das Tamareiras"),
    ("jardim_decolores", "Jardim Decolores"),
    ("jardim_floresta", "Jardim Floresta"),
    ("jardim_ipanema", "Jardim Ipanema"),
    ("jardim_nossa_senhora_do_perpetuo_socorro", "Jardim Nossa Senhora do Perpétuo Socorro"),
    ("jardim_novo_horizonte", "Jardim Novo Horizonte"),
    ("jardim_primavera", "Jardim Primavera"),
    ("jardim_scala", "Jardim Scala"),
    ("nucleo_urbano_anhanguera", "Núcleo Urbano Anhanguera"),
    ("parque_serra_branca", "Parque Serra Branca"),
    ("recanto_do_lago", "Recanto do Lago"),
    ("residencial_alto_do_cerrado_i", "Residencial Alto do Cerrado I"),
    ("residencial_alto_do_cerrado_ii", "Residencial Alto do Cerrado II"),
    ("residencial_araguaia", "Residencial Araguaia"),
    ("residencial_das_neves", "Residencial das Neves"),
    ("residencial_jardim_da_luz", "Residencial Jardim da Luz"),
    ("residencial_maria_monteiro", "Residencial Maria Monteiro"),
    ("residencial_marise", "Residencial Marise"),
    ("residencial_melk", "Residencial Melk"),
    ("residencial_monte_cristo", "Residencial Monte Cristo"),
    ("residencial_moraes", "Residencial Moraes"),
    ("residencial_nova_canaa", "Residencial Nova Canaã"),
    ("residencial_pai_eterno", "Residencial Pai Eterno"),
    ("residencial_paineiras", "Residencial Paineiras"),
    ("residencial_renata_park", "Residencial Renata Park"),
    ("residencial_rosa_morena", "Residencial Rosa Morena"),
    ("residencial_santa_fe", "Residencial Santa Fé"),
    ("residencial_sao_bernardo_ii", "Residencial São Bernardo II"),
    ("residencial_sao_francisco_i", "Residencial São Francisco I"),
    ("residencial_setor_da_mansoes", "Residencial Setor da Mansões"),
    ("residencial_solar_sao_francisco_ii", "Residencial Solar São Francisco II"),
    ("residencial_terra_santa", "Residencial Terra Santa"),
    ("residencial_vieira", "Residencial Vieira"),
    ("santuario", "Santuário"),
    ("setor_abrao_manoel", "Setor Abrão Manoel"),
    ("setor_ana_rosa", "Setor Ana Rosa"),
    ("setor_barcelos", "Setor Barcelos"),
    ("setor_bela_vista", "Setor Bela Vista"),
    ("setor_carvelo", "Setor Carvelo"),
    ("setor_cristina", "Setor Cristina"),
    ("setor_cristina_ii", "Setor Cristina II"),
    ("setor_cristina_ii_expansao", "Setor Cristina II Expansão"),
    ("setor_dos_bandeirantes", "Setor dos Bandeirantes"),
    ("setor_estrela_do_oriente", "Setor Estrela do Oriente"),
    ("setor_jardim_imperial", "Setor Jardim Imperial"),
    ("setor_jardim_marista", "Setor Jardim Marista"),
    ("setor_laguna_parque", "Setor Laguna Parque"),
    ("setor_mariapolis", "Setor Mariápolis"),
    ("setor_maysa", "Setor Maysa"),
    ("setor_monte_sinai", "Setor Monte Sinai"),
    ("setor_morada_do_bosque", "Setor Morada do Bosque"),
    ("setor_morada_do_lago", "Setor Morada do Lago"),
    ("setor_novo_paraiso", "Setor Novo Paraíso"),
    ("setor_oeste", "Setor Oeste"),
    ("setor_pai_eterno", "Setor Pai Eterno"),
    ("setor_palmares", "Setor Palmares"),
    ("setor_ponta_kayana", "Setor Ponta Kayana"),
    ("setor_residencial_garavelo_i", "Setor Residencial Garavelo I"),
    ("setor_residencial_garavelo_ii", "Setor Residencial Garavelo II"),
    ("setor_rio_vermelho", "Setor Rio Vermelho"),
    ("setor_samarah", "Setor Samarah"),
    ("setor_sao_sebastiao", "Setor São Sebastião"),
    ("setor_serra_doura_da", "Setor Serra Dourada"),
    ("setor_soares", "Setor Soares"),
    ("setor_sol_dourado", "Setor Sol Dourado"),
    ("setor_solange", "Setor Solange"),
    ("setor_sul", "Setor Sul"),
    ("setor_vale_dos_sonhos", "Setor Vale dos Sonhos"),
    ("setor_vida_nova", "Setor Vida Nova"),
    ("vila_amador", "Vila Amador"),
    ("vila_arco_iris", "Vila Arco-íris"),
    ("vila_augustus", "Vila Augustus"),
    ("vila_barro_preto", "Vila Barro Preto"),
    ("vila_do_sonho", "Vila do Sonho"),
    ("vila_emanuel", "Vila Emanuel"),
    ("vila_guilherme", "Vila Guilherme"),
    ("vila_jardim_salvador", "Vila Jardim Salvador"),
    ("vila_joao_braz", "Vila João Braz"),
    ("vila_jussara", "Vila Jussara"),
    ("vila_maria", "Vila Maria"),
    ("vila_padre_eterno", "Vila Padre Eterno"),
    ("vila_padre_renato", "Vila Padre Renato"),
    ("vila_roberto_monteiro", "Vila Roberto Monteiro"),
    ("vila_santa_ines", "Vila Santa Inês"),
    ("vila_santo_afonso", "Vila Santo Afonso"),
    ("vila_santo_onofre", "Vila Santo Onofre"),
    ("vila_william", "Vila William"),
]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Complaints(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tiítulo')
    description = models.TextField(max_length=500, verbose_name='Descrição')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='complaint_category', verbose_name='Categoria')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='OPEN', verbose_name='Status')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM', verbose_name='Prioridade')
    address = models.CharField(max_length=255, verbose_name='Endereço')
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES, default='selecione_bairro', verbose_name='Bairro')
    photo = models.ImageField(upload_to='complaints/', blank=True, null=True, verbose_name='Foto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    feedback_agency = models.TextField(blank=True, null=True, verbose_name='Resposta do Órgão')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de atualização')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Reclamação'
        verbose_name_plural = 'Reclamações'


class ComplaintsInventory(models.Model):
    complaints_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Solicitações {self.complaints_count}'


#  Sugestões
class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Ideia")
    description = models.TextField(verbose_name="Como isso ajudaria?")
    votes = models.ManyToManyField(User, related_name='suggestion_votes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_votes(self):
        return self.votes.count()

    class Meta:
        ordering = ['-created_at']

    class Meta:
        verbose_name = 'Sugestão'
        verbose_name_plural = 'Sugestões'
