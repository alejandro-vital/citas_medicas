from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creado en'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Actualizado en'
    )
    
    class Meta:
        abstract = True