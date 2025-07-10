from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.citas.repositories import CitaRepository
from apps.citas.models import Doctor
from core.exceptions import BusinessLogicError

class CitaService:
  def __init__(self):
      self.cita_repo = CitaRepository()
  
  def obtener_citas_activas(self):
      return self.citas_repo.obtener_citas_activas()
  
  def obtener_citas_eliminadas(self):
      return self.citas_repo.obtener_citas_eliminadas()
  
  def obtener_cita_por_id(self, cita_id):
      try:
          return self.citas_repo.obtener_cita_por_id(cita_id)
      except:
          raise BusinessLogicError("Cita no encontrada")
  
  def crear_cita(self, cita_data):
      # Validaciones de negocio
      self._validar_datos_cita(cita_data)
      
      # Verificar disponibilidad del doctor
      if self._doctor_disponible(cita_data['doctor'], cita_data['cita_fecha']):
          raise BusinessLogicError("El doctor no está disponible en esa fecha y hora")
      
      return self.citas_repo.crear_cita(cita_data)
  
  def actualizar_cita(self, cita_id, cita_data):
      cita = self.obtener_cita_por_id(cita_id)
      
      if cita.status == 'deleted':
          raise BusinessLogicError("No se puede editar una cita eliminada")
      
      # Validaciones de negocio
      self._validar_datos_cita(cita_data)
      
      # Verificar disponibilidad del doctor (excluyendo la cita actual)
      if self._doctor_disponible(cita_data['doctor'], cita_data['cita_fecha'], cita_id):
          raise BusinessLogicError("El doctor no está disponible en esa fecha y hora")
      
      return self.citas_repo.actualizar_cita(cita_id, cita_data)
  
  def eliminar_cita(self, cita_id, user):
      cita = self.obtener_cita_por_id(cita_id)
      
      if cita.status == 'deleted':
          raise BusinessLogicError("La cita ya está eliminada")
      
      cita.soft_delete(user)
      return cita
  
  def restaurar_cita(self, cita_id):
      cita = self.obtener_cita_por_id(cita_id)
      
      if cita.status != 'deleted':
          raise BusinessLogicError("La cita no está eliminada")
      
      cita.restore()
      return cita
  
  def _validar_datos_cita(self, data):
      # Validar fecha no sea en el pasado
      if data['cita_fecha'] < timezone.now():
          raise BusinessLogicError("La fecha de la cita no puede ser en el pasado")
      
      # Validar horario de trabajo (8 AM - 6 PM)
      hour = data['cita_fecha'].hour
      if hour < 8 or hour >= 18:
          raise BusinessLogicError("Las citas solo se pueden agendar entre 8:00 AM y 6:00 PM")
  
  def _doctor_disponible(self, doctor, cita_fecha, exclude_cita_id=None):
      from datetime import timedelta
      
      # Verificar si hay otra cita del doctor en +/- 30 minutos
      start_time = cita_fecha - timedelta(minutes=30)
      end_time = cita_fecha + timedelta(minutes=30)
      
      query = self.citas_repo.get_active_citas().filter(
          doctor=doctor,
          fecha_hora_cita_fecha__range=(start_time, end_time)
      )
      
      if exclude_cita_id:
          query = query.exclude(id=exclude_cita_id)
      
      return query.exists()
