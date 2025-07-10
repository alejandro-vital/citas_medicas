from django.db.models import Q
from apps.citas.models import Cita
from apps.pacientes.models import Paciente

class CitaRepository:
    @staticmethod
    def obtener_citas_activas():
        return Cita.objects.filter(estado='active').select_related('paciente', 'doctor__usuario')
    
    @staticmethod
    def obtener_citas_eliminadas():
        return Cita.objects.filter(estado='deleted').select_related('paciente', 'doctor__usuario')
    
    @staticmethod
    def obtener_cita_por_id(cita_id):
        return Cita.objects.select_related('paciente', 'doctor__usuario').get(id=cita_id)
    
    @staticmethod
    def buscar_citas(query):
        return Cita.objects.filter(
            Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query) |
            Q(numero_cita__icontains=query) |
            Q(doctor__usuario__first_name__icontains=query) |
            Q(doctor__usuario__last_name__icontains=query) 
        ).select_related('paciente', 'doctor__usuario')
    
    @staticmethod
    def crear_cita(cita_data):
        return Cita.objects.create(**cita_data) 
    
    @staticmethod
    def actualizar_cita(cita_id, cita_data):
        cita = Cita.objects.get(id=cita_id)
        for key, value in cita_data.items():
            setattr(cita, key, value)
        cita.save()
        return cita