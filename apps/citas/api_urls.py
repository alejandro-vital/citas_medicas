from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import CitaViewSet, DoctorViewSet, PacienteViewSet

router = DefaultRouter()
router.register(r'appointments', CitaViewSet, basename='appointment')
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PacienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
]