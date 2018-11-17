# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Usuario(models.Model):
    username = models.OneToOneField(User)
    tipo = models.IntegerField(default=1) # 1 alumno, 2 profesor, 3 admin
    def __unicode__(self):
        return self.username.username


class Maestro(models.Model):
    usuario = models.ForeignKey(Usuario)
    telefono = models.TextField()
    codigo = models.CharField(max_length=20)
    email = models.EmailField()

    def __unicode__(self):
        return self.usuario.username.username


class Materia(models.Model):
    nombre = models.TextField()
    horas = models.IntegerField()  # horas al semestre
    departamento = models.TextField()
    maestro = models.ForeignKey(Maestro)
    hora = models.TimeField()
    aula = models.CharField(max_length=10)
    ciclo = models.CharField(max_length=15)
    codigo = models.CharField(max_length=10)  # para inscribirse al curso

    def __unicode__(self):
        return self.nombre


class Alumno(models.Model):
    codigo = models.CharField(max_length=20)
    usuario = models.ForeignKey(User)
    carrera = models.TextField() # Cambiar
    cicloIngreso = models.DateField()
    telefono = models.TextField()
    email = models.EmailField()

    def __unicode__(self):
        return self.usuario.username

class TareaMateria(models.Model): # Tareas para un curso (materia) en especifico
    materia = models.ForeignKey(Materia)
    titulo = models.CharField(max_length=40)
    descripcion = models.TextField()
    fechaInicio = models.DateField(auto_now=True)
    fechaFin = models.DateField()


class TareaAlumno(models.Model): # Entregas individuales por alumno
    alumno = models.ForeignKey(Alumno)
    tareaMateria = models.ForeignKey(TareaMateria)
    calificacion = models.FloatField(null=True, blank=True)
    entrega = models.DateTimeField(null=True, blank=True)
    comentario = models.TextField(default="Ninguno")
    estatus = models.IntegerField(default=1)  # 1 pendiente, 2 entregado, 3 atrasado


class MateriaAlumno(models.Model):  # MateriaCiclo & alumno (curso)
    materia = models.ForeignKey(Materia)
    alumno = models.ForeignKey(Alumno)
    calificacion = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.materia.nombre
