from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'telefono', 'fecha_nacimiento', 'created_at']
    search_fields = ['nombre', 'apellido', 'email', 'telefono']
    list_filter = ['created_at', 'fecha_nacimiento']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'fecha_nacimiento')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )