from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('Inicio.html', views.home),
    path('Carga.html', views.carga),
    path('cargar/', views.carga, name='carga'),
    path('enviar/', views.EnviarArchivo, name= 'enviar')
]