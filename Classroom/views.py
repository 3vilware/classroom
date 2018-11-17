# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def init(request):
    return render(request, 'index.html')

def studentInit(request):
    return render(request, 'portalAlumno/index.html')