# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from forms import *
from django.core.exceptions import ObjectDoesNotExist
import json

# Create your views here.


def init(request):
    return render(request, 'index.html')

def successResponse(request):
    return render(request, 'success.html')


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
        print t.pk
        try:
            tareaAlumno = TareaAlumno.objects.get(alumno=student.pk, tareaCurso=t.pk)
            tareasAlumno.append(tareaAlumno)
            print t.pk,"Tarea", tareaAlumno.tareaCurso.curso.nombre,tareaAlumno.estatus
        except ObjectDoesNotExist:
            pass

    context = {"cursos": cursos, "tareas":tasks, "nombre":tasks[0].curso.nombre,
               "alumnoTareas":tareasAlumno}
    return render(request, 'portalAlumno/studentCourse.html', context)


def addCourseToStudent(request,codigo,estudianteId):
    print "Curso", codigo
    print "Estudiante", estudianteId

    try:
        estudiante = Alumno.objects.get(pk=estudianteId)
        curso = Curso.objects.get(codigo=codigo)

        newCursoAlumno = CursoAlumno(curso=curso, alumno=estudiante)
        newCursoAlumno.save()

        tareasCurso = TareaCurso.objects.get(curso=curso.pk)

        for tc in tareasCurso:
            newTareaAlumno = TareaAlumno(alumno=estudiante.pk, tareasCurso=tc)
            newCursoAlumno.save()
    except ObjectDoesNotExist:
        pass
        print "No hay no existe"
    except ValueError:
        print "No hay no existe"
        pass



    return HttpResponse([json.dumps({"estatus":"ok"})], content_type="application/json")


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
        return reverse('successResponse')




def createTarea(request):
    if request.method == 'POST':
        formTarea = TareaForm(data=request.POST)
        if formTarea.is_valid():
            formTarea.save()
            print formTarea.cleaned_data["curso"]
            curso = Curso.objects.get(pk=formTarea.cleaned_data["curso"].pk)
            newTareaCurso = TareaCurso.objects.last()
            tareaParaAlumnos = CursoAlumno.objects.filter(curso=curso)
            for ta in tareaParaAlumnos:
                new = TareaAlumno(alumno=ta.alumno, tareaCurso=newTareaCurso, estatus=1)
                new.save()
            return teacherInit(request)
    else:
        formTarea = TareaForm()
        student = Alumno.objects.first()
        cursos = CursoAlumno.objects.filter(alumno=student.pk)

        context = {"cursos": cursos, "form": formTarea}
        return render(request,'portalMaestros/createTarea.html', context)


def createCurso(request):
    if request.method == 'POST':
        formCurso = CursoForm(data=request.POST)
        if formCurso.is_valid():
            formCurso.save()
            return teacherInit(request)
    else:
        formCurso = CursoForm()
        student = Alumno.objects.first()
        cursos = CursoAlumno.objects.filter(alumno=student.pk)

        context = {"cursos": cursos, "form": formCurso}
        return render(request,'portalMaestros/createTarea.html', context)


def deleteTarea(request, pk, cursoid):
    deleteable = TareaCurso.objects.get(pk=pk)
    deleteable.delete()

    return teacherCourse(request, cursoid)

