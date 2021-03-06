"""day77_class URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^class_list/',views.class_list),
    url(r'^add_class/',views.add_class),
    url(r'^edit_class/(\d+)/',views.edit_class),

    url(r'^student_list/',views.student_list),
    url(r'^add_student/',views.add_student),
    url(r'^edit_student/(\d+)',views.edit_student),

    url(r'^teacher_list/',views.teacher_list),
    url(r'^add_teacher/',views.add_teacher),
    url(r'^edit_teacher/(\d+)',views.edit_teacher),

    url(r'^f2',views.f2),
    url(r'^test/', views.test),

]