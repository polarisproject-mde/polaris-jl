# 📡 Ejemplos de Uso de la API

## 🔐 Autenticación

### Login con JWT

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "estudiante@ejemplo.com",
    "password": "contraseña123"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImVtYWlsIjoiZXN0dWRpYW50ZUBlamVtcGxvLmNvbSIsInJvbCI6ImVzdHVkaWFudGUiLCJleHAiOjE3MzY3MTY4MDB9.xyz...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "estudiante@ejemplo.com",
    "rol": "estudiante"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Email o contraseña incorrectos"
}
```

### Registro de Nuevo Usuario

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "email": "maria@ejemplo.com",
    "rol": "estudiante",
    "password": "contraseña456"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "nombre": "María García",
    "email": "maria@ejemplo.com",
    "rol": "estudiante"
  }
}
```

### Obtener Info del Usuario Autenticado

**Request:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "gmail": "estudiante@ejemplo.com",
  "rol": "estudiante"
}
```

### Cambiar Contraseña

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/change-password \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "current_password=antigua123&new_password=nueva456&confirm_password=nueva456"
```

**Response (200 OK):**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

---

## 👤 Gestión de Usuarios

### Obtener Información del Usuario

**Request:**
```bash
curl -X GET http://localhost:8000/api/usuario/info \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "estudiante@ejemplo.com",
  "rol": "estudiante"
}
```

### Obtener Estadísticas del Usuario

**Request:**
```bash
curl -X GET http://localhost:8000/api/usuario/estadisticas \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "total_tests": 5,
  "ultimo_test": {
    "tipo": "general",
    "fecha": "2025-01-15T10:30:00"
  },
  "area_mas_fuerte": "Desarrollador/a de Software"
}
```

### Obtener Dimensiones Vocacionales

**Request:**
```bash
curl -X GET http://localhost:8000/api/usuario/dimensiones \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "success": true,
  "dimensiones": {
    "tecnologia": 85.5,
    "programacion": 92.0,
    "logica": 78.3,
    "creatividad": 65.8,
    "analitico": 88.2
  },
  "fecha_ultimo_test": "2025-01-15T10:30:00"
}
```

---

## 💬 Foro de Comentarios

### Obtener Comentarios

**Sin filtros:**
```bash
curl -X GET "http://localhost:8000/api/comentarios"
```

**Con filtros:**
```bash
# Por tema
curl -X GET "http://localhost:8000/api/comentarios?tema=tecnologia"

# Ordenados por popularidad
curl -X GET "http://localhost:8000/api/comentarios?orden=popular"

# Con paginación
curl -X GET "http://localhost:8000/api/comentarios?limit=20&offset=0"
```

**Response:**
```json
{
  "comentarios": [
    {
      "id": 1,
      "nombre": "Ana López",
      "tema": "tecnologia",
      "contenido": "¿Alguien sabe cuál es mejor: ingeniería de software o sistemas?",
      "fecha_creacion": "2025-01-15T14:20:00",
      "fecha_actualizacion": "2025-01-15T14:20:00",
      "likes": 15
    }
  ],
  "total": 50,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

### Crear Comentario

**Request:**
```bash
curl -X POST http://localhost:8000/api/comentarios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos Ruiz",
    "tema": "ingenieria",
    "contenido": "Estoy considerando estudiar ingeniería civil. ¿Alguien tiene experiencia?"
  }'
```

**Response (200 OK):**
```json
{
  "id": 51,
  "nombre": "Carlos Ruiz",
  "tema": "ingenieria",
  "contenido": "Estoy considerando estudiar ingeniería civil. ¿Alguien tiene experiencia?",
  "fecha_creacion": "2025-01-15T15:00:00",
  "fecha_actualizacion": "2025-01-15T15:00:00",
  "likes": 0
}
```

### Dar Like a Comentario

**Request:**
```bash
curl -X POST http://localhost:8000/api/comentarios/51/like
```

**Response:**
```json
{
  "likes": 1
}
```

### Actualizar Comentario

**Request:**
```bash
curl -X PUT http://localhost:8000/api/comentarios/51 \
  -H "Content-Type: application/json" \
  -d '{
    "contenido": "Estoy considerando estudiar ingeniería civil o ambiental. ¿Alguien tiene experiencia?",
    "tema": "ingenieria"
  }'
```

### Eliminar Comentario

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/comentarios/51
```

**Response:**
```json
{
  "message": "Comentario eliminado correctamente",
  "id": 51
}
```

### Obtener Temas Populares

**Request:**
```bash
curl -X GET http://localhost:8000/api/temas-populares?limit=5
```

**Response:**
```json
[
  {
    "tema": "tecnologia",
    "nombre_display": "Tecnología",
    "contador": 125
  },
  {
    "tema": "ingenieria",
    "nombre_display": "Ingeniería",
    "contador": 98
  }
]
```

---

## 🎓 Programas Académicos

### Obtener Lista de Programas

**Request:**
```bash
curl -X GET http://localhost:8000/api/programas
```

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Ingeniería de Sistemas",
    "universidad_id": 10,
    "universidad_nombre": "Universidad Nacional",
    "universidad_sigla": "UNAL",
    "universidad_website": "https://unal.edu.co",
    "tipo_universidad": "Pública",
    "ciudad": "Bogotá",
    "departamento": "Cundinamarca",
    "area_nombre": "Ingeniería",
    "area_color": "#3498DB",
    "area_icono": "⚙️",
    "duracion_semestres": 10,
    "creditos": 160,
    "modalidades": ["Presencial", "Virtual"]
  }
]
```

### Obtener Detalle de Programa

**Request:**
```bash
curl -X GET http://localhost:8000/api/programas/1
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Ingeniería de Sistemas",
  "codigo_snies": "12345",
  "universidad_id": 10,
  "universidad_nombre": "Universidad Nacional",
  "universidad_sigla": "UNAL",
  "universidad_website": "https://unal.edu.co",
  "universidad_direccion": "Cra 45 # 26-85",
  "universidad_telefono": "3165000",
  "universidad_email": "admisiones@unal.edu.co",
  "tipo_universidad": "Pública",
  "ciudad": "Bogotá",
  "departamento": "Cundinamarca",
  "area_nombre": "Ingeniería",
  "area_color": "#3498DB",
  "area_icono": "⚙️",
  "duracion_semestres": 10,
  "creditos": 160,
  "titulo_otorgado": "Ingeniero de Sistemas",
  "descripcion": "Programa orientado al desarrollo de software...",
  "perfil_profesional": "El egresado será capaz de...",
  "campo_laboral": "Empresas de tecnología, startups...",
  "costo_semestre": 2500000,
  "modalidades": ["Presencial", "Virtual"],
  "campus": [
    {
      "id": 1,
      "nombre": "Campus Principal",
      "direccion": "Cra 45 # 26-85",
      "ciudad": "Bogotá",
      "telefono": "3165000",
      "es_principal": true
    }
  ]
}
```

### Obtener Universidades

**Request:**
```bash
curl -X GET http://localhost:8000/api/universidades
```

**Response:**
```json
[
  {
    "id": 10,
    "nombre": "Universidad Nacional de Colombia",
    "sigla": "UNAL",
    "tipo_universidad": "Pública"
  }
]
```

### Obtener Áreas de Conocimiento

**Request:**
```bash
curl -X GET http://localhost:8000/api/areas
```

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Ingeniería",
    "descripcion": "Carreras de ingeniería y tecnología",
    "color_hex": "#3498DB",
    "icono": "⚙️"
  }
]
```

### Obtener Modalidades

**Request:**
```bash
curl -X GET http://localhost:8000/api/modalidades
```

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Presencial",
    "descripcion": "Clases presenciales en campus"
  },
  {
    "id": 2,
    "nombre": "Virtual",
    "descripcion": "Clases 100% online"
  }
]
```

---

## 🧪 Ejemplos con JavaScript (Frontend)

### Login y Guardar Token

```javascript
async function login(email, password) {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Guardar token en localStorage
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  } else {
    throw new Error(data.detail);
  }
}
```

### Hacer Request Autenticado

```javascript
async function getUserInfo() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/api/auth/me', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    return await response.json();
  } else if (response.status === 401) {
    // Token expirado, redirigir a login
    window.location.href = '/login';
  } else {
    throw new Error('Error al obtener información del usuario');
  }
}
```

### Crear Comentario

```javascript
async function createComment(nombre, tema, contenido) {
  const response = await fetch('http://localhost:8000/api/comentarios', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ nombre, tema, contenido })
  });
  
  if (response.ok) {
    return await response.json();
  } else {
    const error = await response.json();
    throw new Error(error.detail);
  }
}
```

---

## 🐍 Ejemplos con Python (Cliente)

### Cliente Python con requests

```python
import requests

BASE_URL = "http://localhost:8000"

class VocacionalAPI:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
    
    def login(self, email, password):
        """Login y guardar token"""
        response = self.session.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
            return data["user"]
        else:
            raise Exception(f"Login failed: {response.json()['detail']}")
    
    def get_user_info(self):
        """Obtener info del usuario"""
        response = self.session.get(f"{BASE_URL}/api/auth/me")
        response.raise_for_status()
        return response.json()
    
    def get_programs(self):
        """Obtener lista de programas"""
        response = self.session.get(f"{BASE_URL}/api/programas")
        response.raise_for_status()
        return response.json()
    
    def create_comment(self, nombre, tema, contenido):
        """Crear comentario en foro"""
        response = self.session.post(
            f"{BASE_URL}/api/comentarios",
            json={
                "nombre": nombre,
                "tema": tema,
                "contenido": contenido
            }
        )
        response.raise_for_status()
        return response.json()

# Uso
api = VocacionalAPI()
user = api.login("estudiante@ejemplo.com", "contraseña123")
print(f"Logged in as: {user['nombre']}")

programs = api.get_programs()
print(f"Found {len(programs)} programs")
```

---

## 📱 Ejemplo con App Móvil (React Native)

```javascript
// api.js
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'https://tu-api.com';

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para agregar token automáticamente
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password });
    await AsyncStorage.setItem('access_token', response.data.access_token);
    await AsyncStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  },
  
  logout: async () => {
    await AsyncStorage.removeItem('access_token');
    await AsyncStorage.removeItem('user');
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

export const programsAPI = {
  getAll: async () => {
    const response = await api.get('/api/programas');
    return response.data;
  },
  
  getDetail: async (id) => {
    const response = await api.get(`/api/programas/${id}`);
    return response.data;
  },
};
```

---

## 🔒 Seguridad

### Renovar Token (Implementación Futura)

```javascript
// Implementar refresh token en futuras versiones
async function refreshToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data.access_token;
  } else {
    // Refresh token expirado, logout
    logout();
  }
}
```

---

## 📚 Recursos Adicionales

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman Collection**: Importar desde Swagger

**¡Feliz codificación! 🚀**