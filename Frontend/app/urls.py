from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('Inicio.html', views.home),
    path('Carga.html', views.carga),
    path('Datos.html', views.ConsultarDatos),
    path('ResumenFecha.html', views.FiltrarFecha),
    path('ResumenRango.html', views.FiltrarRango),
    path('Prueba.html', views.MensajePrueba),
    path('Documentacion.html', views.Documentacion),
    path('Informacion.html', views.Informacion),
    path('404.html', views.error),
    path('cargar/', views.carga, name='carga'),
    path('enviar/', views.EnviarArchivo, name= 'enviar'),
    path('resetear/', views.ResetearData, name= 'resetear'),
    path('prueba/', views.MensajePrueba, name='prueba')
]