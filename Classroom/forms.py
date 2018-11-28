from django import forms
from models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-md-4', 'type': 'text'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control col-md-4'}),
        }

class RegisterAlumnoForm(forms.ModelForm):
    class Meta():
        model = Alumno
        exclude = ['usuario']


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

