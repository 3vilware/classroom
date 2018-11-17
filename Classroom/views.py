# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *

# Create your views here.


def init(request):
    return render(request, 'index.html')

def studentInit(request):

    student =Alumno.objects.first()
    materiaAlumno = MateriaAlumno.objects.filter(alumno=1)

    listaTareas = []
    for curso in materiaAlumno:
        ta = TareaAlumno.objects.filter(alumno=2)
        listaTareas.append(ta)
    print listaTareas


    tasks = TareaMateria.objects.filter(materia=1)

    context = {"tareas":tasks}
    return render(request, 'portalAlumno/index.html', context)