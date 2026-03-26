from django import forms
from complaints.models import Complaints


class ComplaintsModelForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = 'title', 'description', 'category', 'address', 'sector', 'photo'
