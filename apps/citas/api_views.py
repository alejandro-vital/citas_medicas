from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Cita, Doctor
from .serializers import CitaSerializer, DoctorSerializer, PacienteSerializer
from .services import CitaService
from apps.pacientes.models import Paciente
from core.exceptions import BusinessLogicError

class CitaViewSet(viewsets.ModelViewSet):
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'tipo_cita', 'doctor']
    search_fields = ['paciente__nombre', 'paciente__apellido', 'numero_cita']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cita_service = CitaService()
    
    def get_queryset(self):
        return Cita.objects.select_related('paciente', 'doctor__usuario').order_by('-fecha_hora_cita')
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            cita_data = {
                'paciente': Paciente.objects.get(id=serializer.validated_data['paciente_id']),
                'doctor': Doctor.objects.get(id=serializer.validated_data['doctor_id']),
                'tipo_cita': serializer.validated_data['tipo_cita'],
                'fecha_hora_cita': serializer.validated_data['fecha_hora_cita'],
                'notas': serializer.validated_data.get('notas', ''),
            }
            
            cita = self.cita_service.create_cita(cita_data)
            response_serializer = self.get_serializer(cita)
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except BusinessLogicError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            
            cita_data = {}
            if 'doctor_id' in serializer.validated_data:
                cita_data['doctor'] = Doctor.objects.get(id=serializer.validated_data['doctor_id'])
            if 'tipo_cita' in serializer.validated_data:
                cita_data['tipo_cita'] = serializer.validated_data['tipo_cita']
            if 'fecha_hora_cita' in serializer.validated_data:
                cita_data['fecha_hora_cita'] = serializer.validated_data['fecha_hora_cita']
            if 'notas' in serializer.validated_data:
                cita_data['notas'] = serializer.validated_data['notas']
            
            cita = self.cita_service.update_cita(instance.id, cita_data)
            response_serializer = self.get_serializer(cita)
            
            return Response(response_serializer.data)
            
        except BusinessLogicError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        try:
            cita = self.cita_service.delete_cita(pk, request.user)
            serializer = self.get_serializer(cita)
            return Response(serializer.data)
        except BusinessLogicError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        try:
            cita = self.cita_service.restore_cita(pk)
            serializer = self.get_serializer(cita)
            return Response(serializer.data)
        except BusinessLogicError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        citas = self.cita_service.get_active_citas()
        page = self.paginate_queryset(citas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(citas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def deleted(self, request):
        citas = self.cita_service.get_deleted_citas()
        page = self.paginate_queryset(citas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(citas, many=True)
        return Response(serializer.data)

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by('apellido', 'nombre')
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'apellido', 'email']