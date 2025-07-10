from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['numero_cita', 'paciente', 'doctor', 'tipo_cita', 'fecha_hora_cita', 'estado']
    list_filter = ['estado', 'tipo_cita', 'fecha_hora_cita', 'created_at']
    search_fields = ['numero_cita', 'paciente__nombre', 'paciente__apellido', 'doctor__usuario__first_name', 'doctor__usuario__last_name']
    readonly_fields = ['numero_cita', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('numero_cita', 'paciente', 'doctor', 'tipo_cita', 'fecha_hora_cita')
        }),
        ('Detalles', {
            'fields': ('notas', 'estado')
        }),
        ('Información de Eliminación', {
            'fields': ('fecha_eliminacion', 'eliminado_por'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj:  # Editing an existing object
            readonly_fields.extend(['paciente'])
        return readonly_fields

    actions = ['eliminacion_logica_citas', 'restaurar_citas']
    
    def eliminacion_logica_citas(self, request, queryset):
        for cita in queryset:
            cita.eliminacion_logica(request.user)
        self.message_user(request, f"{queryset.count()} citas eliminadas correctamente.")
    eliminacion_logica_citas.short_description = "Eliminar citas seleccionadas"
    
    def restaurar_citas(self, request, queryset):
        for cita in queryset:
            cita.restaurar()
        self.message_user(request, f"{queryset.count()} citas restauradas correctamente.")
    restaurar_citas.short_description = "Restaurar citas seleccionadas"