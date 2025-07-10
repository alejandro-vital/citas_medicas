from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('citas/', views.CitaListView.as_view(), name='list'),
    path('citas/create/', views.CitaCreateView.as_view(), name='create'),
    path('citas/<int:pk>/', views.CitaDetailView.as_view(), name='detail'),
    path('citas/<int:pk>/edit/', views.CitaUpdateView.as_view(), name='edit'),
    path('citas/<int:pk>/delete/', views.delete_cita, name='delete'),
    path('citas/<int:pk>/restaurar/', views.restaurar_cita, name='restaurar'),
]