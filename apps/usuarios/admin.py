from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad', 'numero_licencia']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'especialidad']