from django.db import models
from django.core.validators import RegexValidator
from core.models import BaseModel

class Paciente(BaseModel):
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    apellido = models.CharField(
        max_length=100,
        verbose_name='Apellido'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    telefono_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número debe estar en formato: '+999999999'. Hasta 10 dígitos."
    )
    telefono = models.CharField(
        validators=[telefono_regex],
        max_length=17,
        verbose_name='Teléfono'
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )
    direccion = models.TextField(
        blank=True,
        verbose_name='Dirección'
    )
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"