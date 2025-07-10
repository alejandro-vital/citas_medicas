from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.citas.repositories import CitaRepository
from apps.citas.models import Doctor
from core.exceptions import BusinessLogicError

class CitaService:
    def __init__(self):
        self.cita_repo = CitaRepository()
    
    def get_active_citas(self):
        return self.cita_repo.obtener_citas_activas()
    
    def get_deleted_citas(self):
        return self.cita_repo.obtener_citas_eliminadas()
    
    def obtener_cita_por_id(self, cita_id):
        try:
            return self.cita_repo.obtener_cita_por_id(cita_id)
        except:
            raise BusinessLogicError("Cita no encontrada")
    
    def create_cita(self, cita_data):
        # Validaciones de negocio
        self._validar_datos_cita(cita_data)
        
        # Verificar disponibilidad del doctor
        if self._doctor_no_disponible(cita_data['doctor'], cita_data['fecha_hora_cita']):
            raise BusinessLogicError("El doctor no está disponible en esa fecha y hora")
        
        return self.cita_repo.crear_cita(cita_data)
    
    def update_cita(self, cita_id, cita_data):
        cita = self.obtener_cita_por_id(cita_id)
        
        if cita.estado == 'deleted':
            raise BusinessLogicError("No se puede editar una cita eliminada")
        
        # Validaciones de negocio
        self._validar_datos_cita(cita_data)
        
        # Verificar disponibilidad del doctor (excluyendo la cita actual)
        if self._doctor_no_disponible(cita_data.get('doctor', cita.doctor), 
                                     cita_data.get('fecha_hora_cita', cita.fecha_hora_cita), 
                                     cita_id):
            raise BusinessLogicError("El doctor no está disponible en esa fecha y hora")
        
        return self.cita_repo.actualizar_cita(cita_id, cita_data)
    
    def delete_cita(self, cita_id, user):
        cita = self.obtener_cita_por_id(cita_id)
        
        if cita.estado == 'deleted':
            raise BusinessLogicError("La cita ya está eliminada")
        
        cita.eliminacion_logica(user)
        return cita
    
    def restaurar_cita(self, cita_id):
        cita = self.obtener_cita_por_id(cita_id)
        
        if cita.estado != 'deleted':
            raise BusinessLogicError("La cita no está eliminada")
        
        cita.restaurar()
        return cita
    
    def _validar_datos_cita(self, data):
        # Validar fecha no sea en el pasado
        fecha_cita = data.get('fecha_hora_cita')
        if fecha_cita and fecha_cita < timezone.now():
            raise BusinessLogicError("La fecha de la cita no puede ser en el pasado")
        
        # Validar horario de trabajo (8 AM - 6 PM)
        if fecha_cita:
            hour = fecha_cita.hour
            if hour < 8 or hour >= 18:
                raise BusinessLogicError("Las citas solo se pueden agendar entre 8:00 AM y 6:00 PM")
    
    def _doctor_no_disponible(self, doctor, fecha_hora_cita, exclude_cita_id=None):
        from datetime import timedelta
        
        # Verificar si hay otra cita del doctor en +/- 30 minutos
        start_time = fecha_hora_cita - timedelta(minutes=30)
        end_time = fecha_hora_cita + timedelta(minutes=30)
        
        query = self.cita_repo.obtener_citas_activas().filter(
            doctor=doctor,
            fecha_hora_cita__range=(start_time, end_time)
        )
        
        if exclude_cita_id:
            query = query.exclude(id=exclude_cita_id)
        
        return query.exists()