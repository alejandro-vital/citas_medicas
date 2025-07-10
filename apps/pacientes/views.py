from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from apps.pacientes.models import Paciente
from apps.pacientes.forms import PacienteForm
from apps.citas.serializers import PacienteSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by('apellido', 'nombre')
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'apellido', 'email']
    
@login_required
def create_paciente_ajax(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return JsonResponse({
                'success': True,
                'paciente_id': paciente.id,
                'paciente_name': paciente.nombre_completo
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})