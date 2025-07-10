from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator

from apps.citas.models import Cita
from apps.citas.forms import CitaForm, CitaBusquedaForm
from apps.citas.services import CitaService
from apps.pacientes.services import PacienteService
from apps.pacientes.models import Paciente
from apps.pacientes.forms import PacienteForm
from core.exceptions import BusinessLogicError

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'citas/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 10
    
    def __init__(self):
        super().__init__()
        self.cita_service = CitaService()
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'active')
        query = self.request.GET.get('query', '')
        
        if status == 'deleted':
            citas = self.cita_service.obtener_citas_eliminadas()
        else:
            citas = self.cita_service.obtener_citas_activas()
        
        if query:
            citas = citas.filter(
                Q(paciente__nombre__icontains=query) |
                Q(paciente__apellido__icontains=query) |
                Q(numero_cita__icontains=query) |
                Q(doctor__usuario__first_name__icontains=query) |
                Q(doctor__usuario__last_name__icontains=query)
            )
        
        return citas
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CitaBusquedaForm(self.request.GET)
        context['estatus_actual'] = self.request.GET.get('status', 'active')
        return context

class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'citas/cita_form.html'
    success_url = reverse_lazy('citas:list')
    
    def __init__(self):
        super().__init__()
        self.cita_service = CitaService()
        self.paciente_service = PacienteService()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = self.paciente_service.obtener_todos_pacientes()
        context['paciente_form'] = PacienteForm()
        return context
    
    def form_valid(self, form):
        try:
            paciente_id = self.request.POST.get('paciente')
            paciente = self.paciente_service.obetener_paciente_por_id(paciente_id)
            
            cita_data = {
                'paciente': paciente,
                'doctor': form.cleaned_data['doctor'],
                'tipo_cita': form.cleaned_data['tipo_cita'],
                'fecha_hora_cita': form.cleaned_data['fecha_hora_cita'],
                'notas': form.cleaned_data['notas'],
            }
            
            self.cita_service.create_cita(cita_data)
            messages.success(self.request, 'Cita creada exitosamente.')
            return redirect(self.success_url)
            
        except BusinessLogicError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'citas/cita_form.html'
    success_url = reverse_lazy('citas:list')
    
    def __init__(self):
        super().__init__()
        self.cita_service = CitaService()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Deshabilitar campos que no se pueden editar
        form.fields['paciente'].widget.attrs['readonly'] = True
        form.fields['numero_cita'].widget.attrs['readonly'] = True
        return form
    
    def form_valid(self, form):
        try:
            cita_data = {
                'doctor': form.cleaned_data['doctor'],
                'tipo_cita': form.cleaned_data['tipo_cita'],
                'fecha_hora_cita': form.cleaned_data['fecha_hora_cita'],
                'notas': form.cleaned_data['notas'],
            }
            
            self.cita_service.update_cita(self.object.id, cita_data)
            messages.success(self.request, 'Cita actualizada exitosamente.')
            return redirect(self.success_url)
            
        except BusinessLogicError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'citas/cita_detail.html'
    context_object_name = 'cita'

@login_required
def delete_cita(request, pk):
    cita_service = CitaService()
    
    try:
        cita_service.delete_cita(pk, request.usuario)
        messages.success(request, 'Cita eliminada exitosamente.')
    except BusinessLogicError as e:
        messages.error(request, str(e))
    
    return redirect('citas:list')

@login_required
def restore_cita(request, pk):
    cita_service = CitaService()
    
    try:
        cita_service.restore_cita(pk)
        messages.success(request, 'Cita restaurada exitosamente.')
    except BusinessLogicError as e:
        messages.error(request, str(e))
    
    return redirect('citas:list')

@login_required
def create_paciente_ajax(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return JsonResponse({
                'success': True,
                'paciente_id': paciente.id,
                'paciente_name': paciente.full_name
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})