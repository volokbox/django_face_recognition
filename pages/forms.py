from django import forms
from .models import Escola, Professor, Sala

# Form Escola
class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['ID_Escola', 'Nome', 'Agrupamento', 'Localizacao']

# Form Professor
class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['ID_Professor', 'ID_Escola', 'Nome']

# Form Sala
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['ID_Sala', 'Nome_Sala']
