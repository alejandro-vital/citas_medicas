# 🏥 Sistema de Citas Médicas - Clínica Reina Madre

Un sistema de gestión de citas médicas en Django, que permite administrar pacientes, doctores y citas de manera eficiente desarrollado para una prueba tecnica.

## 📋 Descripción del Proyecto

Este es un **monolito full-stack** que combina tanto el frontend como el backend en una sola aplicación Django. La aplicación utiliza:

- **Backend**: Django con arquitectura por capas (models, views, services, repositories)
- **Frontend**: Templates HTML con Tailwind CSS y JavaScript vanilla
- **Base de datos**: SQLite (desarrollo) - fácilmente configurable para PostgreSQL/MySQL
- **Admin**: Panel administrativo nativo de Django
- **API REST**: Endpoints adicionales para integración externa (Para que se realicen pruebas con postman)

## 🛠️ Tecnologías Utilizadas

- **Django** - Framework web principal
- **Django REST Framework** - API REST
- **SQLite** - Base de datos
- **Tailwind CSS** - Framework CSS
- **Font Awesome** - Iconografía

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio
```bash
git clone https://github.com/alejandro-vital/citas_medicas.git
cd citas-medicas
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install django djangorestframework django-filter django-cors-headers django-extensions
```

### 4. Configurar la base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Cargar datos de ejemplo (opcional)
```bash
python manage.py create_sample_data
```

### 7. Ejecutar el servidor
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## 🖥️ Estructura del Proyecto

```
sistema-citas-medicas/
├── apps/
│   ├── citas/           # Gestión de citas y doctores
│   ├── pacientes/       # Gestión de pacientes
│   └── usuarios/        # Autenticación y usuarios
├── config/              # Configuración principal
├── core/                # Utilidades compartidas
├── templates/           # Templates HTML
└── static/              # Archivos estáticos
```

## 🎯 Funcionalidades Principales

### 💻 Aplicación Web (Monolito)
- **Dashboard principal** con estadísticas
- **Gestión de citas**: Crear, editar, eliminar, restaurar
- **Gestión de pacientes**: CRUD completo
- **Sistema de autenticación** personalizado
- **Paginación** automática
- **Interfaz** con Tailwind CSS

### 🔧 Panel de Administración Django
Accede al admin en: `http://127.0.0.1:8000/admin/`

**Características:**
- Gestión completa de todos los modelos
- Filtros y búsquedas avanzadas
- Acciones masivas (eliminar/restaurar citas)
- Interfaz intuitiva para administradores

### 🌐 API REST

El sistema incluye una API REST para integración con aplicaciones externas.

**Base URL**: `http://127.0.0.1:8000/api/`

#### Autenticación
```bash
# Obtener token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "tu_password"}'

# Respuesta
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

#### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/pacientes-api/` | Listar pacientes |
| `POST` | `/api/pacientes-api/` | Crear paciente |
| `GET` | `/api/pacientes-api/{id}/` | Ver paciente |
| `PUT/PATCH` | `/api/pacientes-api/{id}/` | Actualizar paciente |
| `DELETE` | `/api/pacientes-api/{id}/` | Eliminar paciente |
| `GET` | `/api/doctores-api/` | Listar doctores |
| `GET` | `/api/doctores-api/{id}/` | Ver doctor |
| `GET` | `/api/citas-api/` | Listar citas |
| `POST` | `/api/citas-api/` | Crear cita |
| `GET` | `/api/citas-api/{id}/` | Ver cita |
| `PUT/PATCH` | `/api/citas-api/{id}/` | Actualizar cita |
| `POST` | `/api/citas-api/{id}/soft_delete/` | Eliminar cita |
| `POST` | `/api/citas-api/{id}/restore/` | Restaurar cita |
| `GET` | `/api/citas-api/active/` | Citas activas |
| `GET` | `/api/citas-api/deleted/` | Citas eliminadas |

## 🧪 Ejemplos de Uso con Postman

### 1. Obtener Token de Autenticación
**POST** `http://127.0.0.1:8000/api/auth/token/`
```json
{
    "username": "admin",
    "password": "tu_password"
}
```

### 2. Crear un Paciente
**POST** `http://127.0.0.1:8000/api/pacientes-api/`
**Headers**: `Authorization: Token tu_token_aqui`
```json
{
    "nombre": "María",
    "apellido": "González",
    "email": "maria.gonzalez@email.com",
    "telefono": "+521234567890",
    "fecha_nacimiento": "1985-03-20",
    "direccion": "Av. Madero 789, Morelia, Michoacán"
}
```

### 3. Listar Doctores
**GET** `http://127.0.0.1:8000/api/doctores-api/`
**Headers**: `Authorization: Token tu_token_aqui`

### 4. Crear una Cita
**POST** `http://127.0.0.1:8000/api/citas-api/`
**Headers**: `Authorization: Token tu_token_aqui`
```json
{
    "paciente_id": 1,
    "doctor_id": 1,
    "tipo_cita": "consulta",
    "fecha_hora_cita": "2024-12-20T15:30:00",
    "notas": "Primera consulta"
}
```

### 5. Buscar Pacientes
**GET** `http://127.0.0.1:8000/api/pacientes-api/?search=María`
**Headers**: `Authorization: Token tu_token_aqui`

## 🗄️ Modelos de Datos

### Paciente
- Nombre, apellido, email, teléfono
- Fecha de nacimiento, dirección
- Timestamps de creación/actualización

### Doctor
- Relación con Usuario de Django
- Especialidad, número de licencia
- Timestamps de creación/actualización

### Cita
- Relación con Paciente y Doctor
- Número único de cita (auto-generado)
- Tipo de cita (consulta, servicio, tratamiento, etc.)
- Fecha y hora, notas
- Estado (activa, eliminada, completada, cancelada)
- Soft delete con información de eliminación

## 🔐 Usuarios y Permisos

### Autenticación
- Sistema de login/logout personalizado
- Sesiones de Django
- Tokens para API REST
- Redirección inteligente post-login

## 🎨 Interfaz de Usuario

### Diseño
- **Interfaz** con Tailwind CSS
- **Iconografía** con Font Awesome
- **Colores**: Esquema azul/verde/rojo intuitivo
- **Tipografía**: Limpia y legible

### Características UX
- **Mensajes flash** para feedback al usuario
- **Modales** para acciones rápidas
- **Confirmaciones** para acciones destructivas
- **Búsqueda en tiempo real**
- **Paginación** automática


## 🔧 Configuración Avanzada

### Variables de Entorno (Opcional)
```bash
export DEBUG=True
export SECRET_KEY='tu-secret-key-aqui'
export DATABASE_URL='sqlite:///db.sqlite3'
```
---
