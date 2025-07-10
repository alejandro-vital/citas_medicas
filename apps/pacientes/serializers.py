from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'direccion', 'nombre_completo']
        read_only_fields = ['nombre_completo']
