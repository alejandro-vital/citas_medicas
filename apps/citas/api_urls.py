from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import CitaViewSet
from apps.pacientes.views import PacienteViewSet
from apps.usuarios.views import DoctorViewSet

router = DefaultRouter()
router.register(r'citas-api', CitaViewSet, basename='citas-api')
router.register(r'doctores-api', DoctorViewSet)
router.register(r'pacientes-api', PacienteViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('auth/token/', obtain_auth_token, name='api_token_auth'),
  
]