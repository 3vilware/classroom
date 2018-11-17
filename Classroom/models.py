# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Usuario(models.Model):
    username = models.OneToOneField(User)
    tipo = models.IntegerField(default=1) # 1 alumno, 2 profesor, 3 admin


class Maestro(models.Model):
    usuario = models.ForeignKey(Usuario)
    telefono = models.TextField()
    codigo = models.CharField(max_length=20)
    email = models.EmailField()


class Materia(models.Model):
    nombre = models.TextField()
    horas = models.TimeField()  # horas al semestre
    codigo = models.CharField(max_length=10)
    departamento = models.TextField()

class MateriaCiclo(models.Model):
    materia = models.ForeignKey(Materia)
    maestro = models.ForeignKey(Maestro)
    hora = models.TimeField()
    aula = models.CharField(max_length=10)
    ciclo = models.CharField(max_length=15)
    codigo = models.CharField(max_length=10)  # para inscribirse al curso

class Tarea(models.Model):
    materiaCiclo = models.ForeignKey(MateriaCiclo)
    descripcion = models.TextField()
    fechaInicio = models.DateField(auto_now=True)
    fechaFin = models.DateField()

class Alumno(models.Model):
    codigo = models.CharField(max_length=20)
    usuario = models.ForeignKey(User)
    carrera = models.TextField() # Cambiar
    cicloIngreso = models.DateField()
    telefono = models.TextField()
    email = models.EmailField()


class TareaAlumno(models.Model):
    alumno = models.ForeignKey(Alumno)
    tarea = models.ForeignKey(Tarea)
    calificacion = models.FloatField(null=True)
    entrega = models.DateTimeField(null=True)
    comentario = models.TextField(default="Ninguno")


class MateriaAlumno(models.Model):  # MateriaCiclo & alumno (curso)
    materiaCiclo = models.ForeignKey(MateriaCiclo)
    alumno = models.ForeignKey(Alumno)
    calificacion = models.FloatField(null=True)
