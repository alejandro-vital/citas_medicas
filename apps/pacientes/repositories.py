from django.db.models import Q
from apps.pacientes.models import Paciente


class PacienteRepository:
    @staticmethod
    def obtener_todos_los_pacientes():
        return Paciente.objects.all().order_by('apellido', 'nombre')
    
    @staticmethod
    def obtener_paciente_por_id(paciente_id):
        return Paciente.objects.get(id=paciente_id)
    
    @staticmethod
    def buscar_pacientes(query):
        return Paciente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query)
        )