from rest_framework import serializers
from .models import Cita, Doctor
from apps.pacientes.models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'direccion', 'nombre_completo']
        read_only_fields = ['nombre_completo']

class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'especialidad', 'numero_licencia']

class CitaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    paciente_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    cita_type_display = serializers.CharField(source='get_cita_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Cita
        fields = [
            'id', 'numero_cita', 'paciente', 'doctor', 'paciente_id', 'doctor_id',
            'tipo_cita', 'cita_type_display', 'fecha_hora_cita', 
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