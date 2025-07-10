from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.pacientes.models import Paciente
from core.models import BaseModel

class Doctor(BaseModel):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_prerfil'
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

class Cita(BaseModel):
    TIPOS_CITA = [
        ('consulta', 'Consulta'),
        ('servicio', 'Servicio'),
        ('tratamiento', 'Tratamiento'),
        ('cirugia', 'Cirugía'),
        ('emergencia', 'Emergencia'),
    ]
    
    ESTADOS_CHOICES = [
        ('active', 'Activa'),
        ('deleted', 'Eliminada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    
    numero_cita = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Cita',
        editable=False
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name='Paciente',
        editable=False
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name='Doctor'
    )
    tipo_cita = models.CharField(
        max_length=20,
        choices=TIPOS_CITA,
        verbose_name='Tipo de Cita'
    )
    fecha_hora_cita = models.DateTimeField(
        verbose_name='Fecha y Hora de la Cita'
    )
    notas = models.TextField(
        blank=True,
        verbose_name='Notas'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_CHOICES,
        default='active',
        verbose_name='Estado'
    )
    fecha_eliminacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Eliminación'
    )
    eliminado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='citas_eliminadas',
        verbose_name='Eliminado por'
    )
    
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha_hora_cita']
    
    def __str__(self):
        return f"Cita #{self.numero_cita} - {self.paciente.nombre_completo}"
    
    def clean(self):
        if self.fecha_hora_cita and self.fecha_hora_cita < timezone.now():
            raise ValidationError('La fecha de la cita no puede ser en el pasado.')
    
    def save(self, *args, **kwargs):
        if not self.numero_cita:
            self.numero_cita = self.generar_numero_cita()
        super().save(*args, **kwargs)
    
    def generar_numero_cita(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def sotf_eliminar(self, usuario):
        self.estado = 'deleted'
        self.fecha_eliminacion = timezone.now()
        self.eliminado_por = usuario
        self.save()
    
    def restaurar(self):
        self.estado = 'active'
        self.fecha_eliminacion = None
        self.eliminado_por = None
        self.save()