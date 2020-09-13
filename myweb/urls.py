"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from mainsite.views import *
import templates

urlpatterns = [
    path('',index),
    path('admin/', admin.site.urls),
    path('login/', login),
    path('logout/', logout),
    path('userpro/', userpro),
    path('myml/', myml),
    path('mypy/', mypy),
    path('teacher/', teacher),
    path('neweek/', neweek),
    path('delweek/', delweek),
    path('scoring/<str:team>/<str:week>/',scoring),
    path('teachlog/',teachlog),
    path('teachlogout/',teachlogout),
    path('changepsw/',changepsw),
    path('searchname/',searchname),
    path('searchid/',searchid),


    path('test/',test),
    path('testadd/',testadd),

]
