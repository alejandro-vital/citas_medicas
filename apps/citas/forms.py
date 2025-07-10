from django import forms
from django.utils import timezone
from apps.citas.models import Cita, Doctor

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'tipo_cita', 'fecha_hora_cita', 'notas']
        widgets = {
            'fecha_hora_cita': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_cita': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.select_related('usuario')
        self.fields['fecha_hora_cita'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    def clean_fecha_hora_cita(self):
        fecha_hora_cita = self.cleaned_data['fecha_hora_cita']
        
        if fecha_hora_cita < timezone.now():
            raise forms.ValidationError("La fecha de la cita no puede ser en el pasado.")
        
        # Validar horario de trabajo
        hour = fecha_hora_cita.hour
        if hour < 8 or hour >= 18:
            raise forms.ValidationError("Las citas solo se pueden agendar entre 8:00 AM y 6:00 PM.")
        
        return fecha_hora_cita

class CitaBusquedaForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por paciente, doctor o número de cita...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('active', 'Activas'),
            ('deleted', 'Eliminadas'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )