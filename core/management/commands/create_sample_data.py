# Primero necesitas crear esta estructura de carpetas:
# core/management/
# core/management/__init__.py
# core/management/commands/
# core/management/commands/__init__.py
# core/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
import random

from apps.pacientes.models import Paciente
from apps.citas.models import Doctor, Cita

class Command(BaseCommand):
    help = 'Crear datos de ejemplo para el sistema'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--pacientes',
            type=int,
            default=10,
            help='Número de pacientes a crear'
        )
        parser.add_argument(
            '--doctores',  # Corregido de 'doctors'
            type=int,
            default=3,
            help='Número de doctores a crear'
        )
        parser.add_argument(
            '--citas',  # Corregido de 'appointments'
            type=int,
            default=20,
            help='Número de citas a crear'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Creando datos de ejemplo...')
        
        # Crear usuario administrador
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@clinic.com',
                password='admin123',
                first_name='Admin',
                last_name='Sistema'
            )
            self.stdout.write(f'Usuario admin creado: admin/admin123')
        
        # Crear doctores
        especialidades = ['Cardiología', 'Dermatología', 'Pediatría', 'Neurología', 'Traumatología']
        doctores_data = [
            {
                'username': 'dr_garcia', 
                'first_name': 'Carlos', 
                'last_name': 'García', 
                'especialidad': 'Cardiología'
            },
            {
                'username': 'dra_lopez', 
                'first_name': 'María', 
                'last_name': 'López', 
                'especialidad': 'Dermatología'
            },
            {
                'username': 'dr_martinez', 
                'first_name': 'José', 
                'last_name': 'Martínez', 
                'especialidad': 'Pediatría'
            },
        ]
        
        for i in range(options['doctores']):
            if i < len(doctores_data):
                doctor_data = doctores_data[i]
            else:
                doctor_data = {
                    'username': f'doctor_{i+1}',
                    'first_name': f'Doctor{i+1}',
                    'last_name': f'Apellido{i+1}',
                    'especialidad': random.choice(especialidades)
                }
            
            if not User.objects.filter(username=doctor_data['username']).exists():
                user = User.objects.create_user(
                    username=doctor_data['username'],
                    email=f"{doctor_data['username']}@clinic.com",
                    password='doctor123',
                    first_name=doctor_data['first_name'],
                    last_name=doctor_data['last_name']
                )
                
                Doctor.objects.create(
                    usuario=user,  # Corregido de 'user'
                    especialidad=doctor_data['especialidad'],  # Corregido de 'specialization'
                    numero_licencia=f'LIC{1000 + i}'  # Corregido de 'license_number'
                )
                
                self.stdout.write(f'Doctor creado: {doctor_data["username"]}/doctor123')
        
        # Crear pacientes
        nombres = ['Ana', 'Luis', 'Carmen', 'Pedro', 'Isabel', 'Miguel', 'Rosa', 'Antonio', 'Elena', 'Francisco']
        apellidos = ['González', 'Rodríguez', 'Pérez', 'Sánchez', 'Martín', 'López', 'García', 'Díaz', 'Ruiz', 'Hernández']
        
        for i in range(options['pacientes']):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            
            email = f'{nombre.lower()}.{apellido.lower()}{i}@email.com'
            if not Paciente.objects.filter(email=email).exists():
                Paciente.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    telefono=f'+52{random.randint(1000000000, 9999999999)}',
                    fecha_nacimiento=timezone.now().date() - timedelta(days=random.randint(365*20, 365*80)),
                    direccion=f'Calle {random.randint(1, 100)} #{random.randint(1, 999)}, Morelia, Michoacán'
                )
        
        # Crear citas
        pacientes = list(Paciente.objects.all())
        doctores = list(Doctor.objects.all())
        tipos_cita = ['consulta', 'servicio', 'tratamiento', 'cirugia']
        
        if not pacientes:
            self.stdout.write(self.style.ERROR('No hay pacientes disponibles para crear citas'))
            return
            
        if not doctores:
            self.stdout.write(self.style.ERROR('No hay doctores disponibles para crear citas'))
            return
        
        for i in range(options['citas']):
            # Crear citas futuras
            days_ahead = random.randint(1, 30)
            hour = random.randint(8, 17)
            minute = random.choice([0, 30])
            
            fecha_hora_cita = timezone.now() + timedelta(days=days_ahead)
            fecha_hora_cita = fecha_hora_cita.replace(
                hour=hour, 
                minute=minute, 
                second=0, 
                microsecond=0
            )
            
            try:
                Cita.objects.create(
                    paciente=random.choice(pacientes),
                    doctor=random.choice(doctores),
                    tipo_cita=random.choice(tipos_cita),
                    fecha_hora_cita=fecha_hora_cita,
                    notas=f'Cita de ejemplo #{i+1}',  # Corregido de 'notes'
                    estado='active'  # Corregido de 'status'
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Error creando cita {i+1}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Datos de ejemplo creados exitosamente:\n'
                f'- {options["doctores"]} doctores\n'
                f'- {options["pacientes"]} pacientes\n'
                f'- {options["citas"]} citas'
            )
        )