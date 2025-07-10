from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'especialidad', 'numero_licencia']
