from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
  path('ajax/create-paciente/', views.create_paciente_ajax, name='create_paciente_ajax'),
]