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
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


# Create your views here.


def init(request):
    return render(request, 'index.html')


def successResponse(request):
    return render(request, 'success.html')


def studentRegister(request):
    if request.method == 'POST':
        pass
        formRegistro = RegisterAlumnoForm(data=request.POST)
        formUser = UserForm(data=request.POST)
        context = {"form": formRegistro, "formUser": formUser}
        print formUser.errors
        print formRegistro.errors
        if formRegistro.is_valid() and formUser.is_valid():
            print formUser.cleaned_data
            pwd = formUser.cleaned_data.get('password')
            usuario = formUser.save()
            usuario.set_password(pwd)
            usuario.save()
            usuarioInstance = Usuario(username=usuario, tipo=1)
            usuarioInstance.save()
            registro = formRegistro.save(commit=False)
            registro.usuario = usuarioInstance
            registro.save()
            print "Saved"

        return render(request, 'login.html', context)
    else:
        formRegistro = RegisterAlumnoForm()
        formUser = UserForm()
        context = {"form": formRegistro, "formUser": formUser}

        return render(request, 'portalAlumno/registerStudent.html', context)



def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('pass')
        try:
            usuarioSistema = User.objects.get(username=usuario)
        except ObjectDoesNotExist:
            return HttpResponse("Error usuario")

        user = authenticate(username=usuarioSistema.username, password=password)

        if user:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('init'))
        else:
            return HttpResponse("Credenciales incorrectas")

    else:
        return render(request, 'login.html', {})


@login_required
def studentInit(request):
    student =Alumno.objects.first()

    cursos = CursoAlumno.objects.filter(alumno=student.pk)

    context = {"cursos": cursos}
    return render(request, 'portalAlumno/index.html', context)


@login_required
def studentCourse(request, cursoid):
    student = Alumno.objects.first()
    cursos = CursoAlumno.objects.filter(alumno=student.pk)

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
            print t.pk, "Tarea", tareaAlumno.tareaCurso.curso.nombre, tareaAlumno.estatus
        except ObjectDoesNotExist:
            pass

    context = {"cursos": cursos, "tareas": tasks, "nombre": tasks[0].curso.nombre,
               "alumnoTareas": tareasAlumno}
    return render(request, 'portalAlumno/studentCourse.html', context)


def addCourseToStudent(request, codigo, estudianteId):
    print "Curso", codigo
    print "Estudiante", estudianteId

    try:
        estudiante = Alumno.objects.get(pk=estudianteId)
        curso = Curso.objects.get(codigo=codigo)

        newCursoAlumno = CursoAlumno(curso=curso, alumno=estudiante)
        newCursoAlumno.save()

        tareasCurso = TareaCurso.objects.filter(curso=curso.pk)
        print "DEBUG tareasCurso:", tareasCurso
        for tc in tareasCurso:
            print "Nuevo tc", tc.titulo
            newTareaAlumno = TareaAlumno(alumno=estudiante, tareaCurso=tc)
            newTareaAlumno.save()
            print "Success"
    except ObjectDoesNotExist, e:
        pass
        print "Error:", e
    except ValueError, e:
        print "Error:", e
        pass
    except TypeError, e:
        print "Error:", e
        pass

    return HttpResponse([json.dumps({"estatus": "ok"})], content_type="application/json")


def uploadTarea(request):
    if request.method == 'POST':
        file = request.FILES['tareaFile']
        tid = int(request.POST.get('tareaId'))

        try:
            # userObj = User.objects.get(username=request.user)
            # usuario = Usuario.objects.get(username=userObj)
            # student = Alumno.objects.get(usuario=usuario.pk)# Alumno.objects.get(usuario=request.user)
            student = Alumno.objects.first()
            tareaGeneral = TareaCurso.objects.get(pk=tid)
            print student.pk, "&", tareaGeneral.pk
            tareaAlumno = TareaAlumno.objects.get(alumno=student.pk, tareaCurso=tareaGeneral.pk)
            print tareaAlumno.archivo
            tareaAlumno.entrega = timezone.now()
            tareaAlumno.estatus = 2  # Entregado
            tareaAlumno.archivo = file
            tareaAlumno.save()
            print("Tarea alumno:", tareaAlumno.pk)
        except ObjectDoesNotExist, e:
            print "Error:", e

    return HttpResponseRedirect(reverse('init'))

@login_required
def teacherInit(request):
    teacher = Maestro.objects.first()

    cursos = Curso.objects.filter(maestro=teacher.pk)

    context = {"cursos": cursos}
    return render(request, 'portalMaestros/index.html', context)

@login_required
def teacherCourse(request, cursoid):
    teacher = Maestro.objects.first()
    cursos = Curso.objects.filter(maestro=teacher.pk)

    tasks = TareaCurso.objects.filter(curso=cursoid)
    curso = Curso.objects.get(pk=cursoid)

    tareasAlumnos = []
    for tc in tasks:
        ta = TareaAlumno.objects.filter(tareaCurso=tc.pk)
        for t in ta:
            tareasAlumnos.append(t)



    context = {"cursos": cursos, "tareas": tasks, "name": curso.nombre,
               "calificables":tareasAlumnos}
    return render(request, 'portalMaestros/teacherCourse.html', context)


class updateTarea(UpdateView):
    model = TareaCurso
    form_class = TareaForm
    template_name = 'portalMaestros/edit.html'

    # success_url = 'Success'

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
            return HttpResponse("<h4>!Correcto¡</h4>")
    else:
        formTarea = TareaForm()
        student = Alumno.objects.first()

        cursos = CursoAlumno.objects.filter(alumno=student.pk)

        context = {"cursos": cursos, "form": formTarea}
        return render(request, 'portalMaestros/createTarea.html', context)


def createCurso(request):
    if request.method == 'POST':
        formCurso = CursoForm(data=request.POST)
        if formCurso.is_valid():
            formCurso.save()
            print "Llego aqui"
            return render(request, 'success.html', {})
        else:
            HttpResponse("Mal")
    else:
        formCurso = CursoForm()
        student = Alumno.objects.first()

        cursos = CursoAlumno.objects.filter(alumno=student.pk)

        context = {"cursos": cursos, "form": formCurso}
        return render(request, 'portalMaestros/createCurso.html', context)


def checkTareaAlumno(request, taid):
    taid = int(taid)
    print "TAID", taid
    try:
        ta = TareaAlumno.objects.get(pk=taid)
        ta.calificacion = 1
        ta.save()
    except ObjectDoesNotExist, e:
        print "Error", e

    return render(request, 'portalMaestros/index.html', {})



def deleteTarea(request, pk, cursoid):
    deleteable = TareaCurso.objects.get(pk=pk)
    deleteable.delete()

    return teacherCourse(request, cursoid)


def deleteCurso(request, cursoid):
    try:
        deleteable = Curso.objects.get(pk=cursoid)
        deleteable.delete()
    except ValueError:
        return teacherInit(request)
    except ObjectDoesNotExist:
        return teacherInit(request)

    return teacherInit(request)


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'login.html', {})
