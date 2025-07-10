from django.contrib import messages
from django.views.generic import  TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.citas.serializers import DoctorSerializer
from apps.usuarios.models import Doctor

  
class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.select_related('usuario').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

  
def logout_view(request):
    """Vista personalizada para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('citas:home')  # Redirige a la página de inicio
    
class LoginView(TemplateView):
    template_name = 'usuarios/login.html'
    
    def get(self, request, *args, **kwargs):
        # Si ya está autenticado, redirigir a inicio
        if request.user.is_authenticated:
            return redirect('citas:home')
        
        context = self.get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.get_full_name() or user.username}!')
                
                # Redirigir según el tipo de usuario
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                elif user.is_staff or user.is_superuser:
                    # Si es staff, dar opción de ir al admin o al inicio
                    return redirect('citas:home')
                else:
                    return redirect('citas:home')
            else:
                messages.error(request, 'Credenciales inválidas.')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
