from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('base.html', views.home),
]