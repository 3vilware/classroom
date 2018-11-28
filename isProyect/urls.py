"""isProyect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Classroom import views
from django.views.generic import TemplateView
from django.conf.urls.static import static

from isProyect import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^init/', views.init, name="init"),
    url(r'^studentPortal/', views.studentInit, name="init"),
    url(r'^studentCourse/(?P<cursoid>.+?)', views.studentCourse, name="studentCourse"),
    url(r'^addCourseToStudent/(?P<codigo>.+?)/(?P<estudianteId>.+?)', views.addCourseToStudent, name="addCourseToStudent"),
    url(r'^uploadFile/', views.uploadTarea, name="uploadFile"),

    #Teacher
    url(r'^teacherInit/', views.teacherInit, name="teacherInit"),
    url(r'^teacherCourse/(?P<cursoid>.+?)', views.teacherCourse, name="teacherCourse"),
    url(r'^teacherEditTask/(?P<pk>.+?)/', views.updateTarea.as_view(), name="teacherEditTask"),
    url(r'^teacherDeleteTask/(?P<pk>.+?)/(?P<cursoid>.+?)', views.deleteTarea, name="teacherDeleteTask"),
    url(r'^teacherDeleteCourse/(?P<cursoid>.+?)', views.deleteCurso, name="teacherDeleteCourse"),
    url(r'^createTeacherTask/', views.createTarea, name="createTeacherTask"),
    url(r'^createTeacherCourse/', views.createCurso, name="createTeacherCourse"),
    url(r'^successResponse/', views.successResponse, name="successResponse"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)