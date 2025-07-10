# apps/appointments/management/__init__.py
# apps/appointments/management/commands/__init__.py

# apps/appointments/management/commands/create_sample_data.py
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
            '--doctors',
            type=int,
            default=3,
            help='Número de doctores a crear'
        )
        parser.add_argument(
            '--appointments',
            type=int,
            default=20,
            help='Número de citas a crear'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Creando datos de ejemplo...')
        
        # Crear usuarios administradores
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
        specializations = ['Cardiología', 'Dermatología', 'Pediatría', 'Neurología', 'Traumatología']
        doctors_data = [
            {'username': 'dr_garcia', 'first_name': 'Carlos', 'last_name': 'García', 'specialization': 'Cardiología'},
            {'username': 'dra_lopez', 'first_name': 'María', 'last_name': 'López', 'specialization': 'Dermatología'},
            {'username': 'dr_martinez', 'first_name': 'José', 'last_name': 'Martínez', 'specialization': 'Pediatría'},
        ]
        
        for i in range(options['doctores']):
            if i < len(doctors_data):
                doctor_data = doctors_data[i]
            else:
                doctor_data = {
                    'username': f'doctor_{i+1}',
                    'first_name': f'Doctor{i+1}',
                    'last_name': f'Apellido{i+1}',
                    'especialidad': random.choice(specializations)
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
                    user=user,
                    specialization=doctor_data['especialidad'],
                    license_number=f'LIC{1000 + i}'
                )
                
                self.stdout.write(f'Doctor creado: {doctor_data["username"]}/doctor123')
        
        # Crear pacientes
        first_names = ['Ana', 'Luis', 'Carmen', 'Pedro', 'Isabel', 'Miguel', 'Rosa', 'Antonio', 'Elena', 'Francisco']
        last_names = ['González', 'Rodríguez', 'Pérez', 'Sánchez', 'Martín', 'López', 'García', 'Díaz', 'Ruiz', 'Hernández']
        
        for i in range(options['pacientes']):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            if not Paciente.objects.filter(email=f'{first_name.lower()}.{last_name.lower()}{i}@email.com').exists():
                Paciente.objects.create(
                    nombre=first_name,
                    apellido=last_name,
                    email=f'{first_name.lower()}.{last_name.lower()}{i}@email.com',
                    telefono=f'+52{random.randint(1000000000, 9999999999)}',
                    fecha_nacimiento=timezone.now().date() - timedelta(days=random.randint(365*20, 365*80)),
                    direccion=f'Calle {random.randint(1, 100)} #{random.randint(1, 999)}, Morelia, Michoacán'
                )
        
        # Crear citas
        pacientes = list(Paciente.objects.all())
        doctors = list(Doctor.objects.all())
        tipo_cita = ['consulta', 'servicio', 'tratamiento', 'cirugia']
        
        for i in range(options['citas']):
            # Crear citas futuras
            days_ahead = random.randint(1, 30)
            hour = random.randint(8, 17)
            minute = random.choice([0, 30])
            
            fecha_hora_cita = timezone.now() + timedelta(days=days_ahead)
            fecha_hora_cita = fecha_hora_cita.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            Cita.objects.create(
                paciente=random.choice(pacientes),
                doctor=random.choice(doctors),
                tipo_cita=random.choice(tipo_cita),
                fecha_hora_cita=fecha_hora_cita,
                notes=f'Cita de ejemplo #{i+1}',
                status='active'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Datos de ejemplo creados exitosamente:\n'
                f'- {options["doctors"]} doctores\n'
                f'- {options["pacientes"]} pacientes\n'
                f'- {options["appointments"]} citas'
            )
        )