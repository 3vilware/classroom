from django import forms
from models import *

class TareaForm(forms.ModelForm):
    class Meta():
        model = TareaCurso
        fields = '__all__'

        widgets = {
            'fechaFin': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
        }


class CursoForm(forms.ModelForm):
    class Meta():
        model = Curso
        fields = '__all__'

        widgets = {
        }