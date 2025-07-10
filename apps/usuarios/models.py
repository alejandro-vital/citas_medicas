from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
class Doctor(BaseModel):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_perfil'
    )
    especialidad = models.CharField(
        max_length=100,
        verbose_name='Especialización'
    )
    numero_licencia = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de Licencia'
    )
    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
    
    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()}"