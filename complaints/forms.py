from django import forms
from complaints.models import Complaints

class ComplaintsModelForm(forms.ModelForm):
    class Meta:
        model = Complaints
        # Mantemos os campos visíveis para o cidadão
        fields = ['title', 'description', 'category', 'address', 'sector', 'photo']
        
        # Adicionamos widgets para melhorar a aparência (opcional, mas recomendado)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o problema detalhadamente...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Ex: Buraco na rua, Entulho na calçada'}),
            'address': forms.TextInput(attrs={'placeholder': 'Rua, Número, Referência'}),
        }

    def __init__(self, *args, **kwargs):
        super(ComplaintsModelForm, self).__init__(*args, **kwargs)
        # Deixa o campo "Selecione o Bairro" como a opção padrão e obrigatória
        self.fields['sector'].empty_label = "Selecione o Bairro"