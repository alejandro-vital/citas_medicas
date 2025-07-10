from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'telefono', 'fecha_nacimiento', 'created_at']
    search_fields = ['first_name', 'apellido', 'email', 'telefono']
    list_filter = ['created_at', 'fecha_nacimiento']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'apellido', 'fecha_nacimiento')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )