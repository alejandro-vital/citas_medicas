from django import forms
from django.utils import timezone
from apps.pacientes.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        
        if fecha_nacimiento >= timezone.now().date():
            raise forms.ValidationError("La fecha de nacimiento debe ser anterior a hoy.")
        
        return fecha_nacimiento

