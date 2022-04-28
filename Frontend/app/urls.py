from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('Inicio.html', views.home),
    path('Carga.html', views.carga),
    path('Datos.html', views.ConsultarDatos),
    path('ResumenFecha.html', views.FiltrarFecha),
    path('cargar/', views.carga, name='carga'),
    path('enviar/', views.EnviarArchivo, name= 'enviar'),
    path('resetear/', views.ResetearData, name= 'resetear'),
]