from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.CitaListView.as_view(), name='list'),
    path('create/', views.CitaCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CitaDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CitaUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.delete_cita, name='delete'),
    path('<int:pk>/restore/', views.restore_cita, name='restore'),
    path('ajax/create-paciente/', views.create_paciente_ajax, name='create_paciente_ajax'),
]