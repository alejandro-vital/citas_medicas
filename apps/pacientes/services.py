from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.pacientes.repositories import PacienteRepository
class PacienteService:
  def __init__(self):
    self.paciente_repo = PacienteRepository()
  
  def obtener_todos_pacientes(self):
    return self.paciente_repo.buscar_pacientes()
  
  def obetener_paciente_por_id(self, paciente_id):
    return self.paciente_repo.obtener_paciente_por_id(paciente_id)
  
  def buscar_pacientes(self, query):
    return self.paciente_repo.buscar_pacientes(query)