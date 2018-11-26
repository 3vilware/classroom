# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from forms import *


# Create your views here.


def init(request):
    return render(request, 'index.html')

def studentInit(request):

    student =Alumno.objects.first()
    cursos = CursoAlumno.objects.filter(alumno=student.pk)

    context = {"cursos":cursos}
    return render(request, 'portalAlumno/index.html', context)


def studentCourse(request, cursoid):
    student = Alumno.objects.first()
    cursos = CursoAlumno.objects.filter(alumno=student.pk)

    tasks = []
    tasks = TareaCurso.objects.filter(curso=cursoid)

    tareasCurso = TareaCurso.objects.filter(curso=cursoid)

    tareasAlumno = []
    for t in tareasCurso:
        tareasAlumno = TareaAlumno.objects.filter(alumno=student.pk, tareaCurso=t.pk)

    for tar in tareasAlumno:
        print tar.tareaCurso.curso, "added a este wey"


    context = {"cursos": cursos, "tareas":tasks, "nombre":tasks[0].curso.nombre,
               "alumnoTareas":tareasAlumno}
    return render(request, 'portalAlumno/studentCourse.html', context)


def teacherInit(request):
    teacher = Maestro.objects.first()

    cursos = Curso.objects.filter(maestro=teacher.pk)

    context = {"cursos": cursos}
    return render(request, 'portalMaestros/index.html', context)


def teacherCourse(request, cursoid):
    teacher = Maestro.objects.first()
    cursos = Curso.objects.filter(maestro=teacher.pk)

    tasks = TareaCurso.objects.filter(curso=cursoid)
    curso = Curso.objects.get(pk=cursoid)

    context = {"cursos": cursos, "tareas":tasks, "name":curso.nombre}
    return render(request, 'portalMaestros/teacherCourse.html', context)


class updateTarea(UpdateView):
    model = TareaCurso
    form_class = TareaForm
    template_name = 'portalMaestros/edit.html'
    #success_url = 'Success'

    def get_success_url(self):
        return reverse('teacherInit')


def createTarea(request):
    if request.method == 'POST':
        formTarea = TareaForm(data=request.POST)
        if formTarea.is_valid():
            formTarea.save()
            return teacherInit(request)
    else:
        formTarea = TareaForm()
        student = Alumno.objects.first()
        cursos = CursoAlumno.objects.filter(alumno=student.pk)

        context = {"cursos": cursos, "form": formTarea}
        return render(request,'portalMaestros/createTarea.html', context)


def deleteTarea(request, pk, cursoid):
    deleteable = TareaCurso.objects.get(pk=pk)
    deleteable.delete()

    return teacherCourse(request, cursoid)
