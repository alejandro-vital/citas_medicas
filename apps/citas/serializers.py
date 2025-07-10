from rest_framework import serializers


from .models import Cita
from apps.pacientes.models import Paciente
from apps.pacientes.serializers import PacienteSerializer
from apps.usuarios.serializers import DoctorSerializer
from apps.usuarios.models import Doctor

class CitaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    paciente_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    tipo_cita_visualizar = serializers.CharField(source='get_tipo_cita_visualizar', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Cita
        fields = [
            'id', 'numero_cita', 'paciente', 'doctor', 'paciente_id', 'doctor_id',
            'tipo_cita', 'tipo_cita_visualizar', 'fecha_hora_cita', 
            'notas', 'estado', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['numero_cita', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        paciente_id = validated_data.pop('paciente_id')
        doctor_id = validated_data.pop('doctor_id')
        
        validated_data['paciente'] = Paciente.objects.get(id=paciente_id)
        validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # No permitir cambiar paciente y número de cita
        validated_data.pop('paciente_id', None)
        
        doctor_id = validated_data.pop('doctor_id', None)
        if doctor_id:
            validated_data['doctor'] = Doctor.objects.get(id=doctor_id)
        
        return super().update(instance, validated_data)