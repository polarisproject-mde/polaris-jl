# 🎓 Plataforma de Orientación Vocacional v2.0

Sistema completo de orientación vocacional con tests, foro, gestión de usuarios y autenticación JWT.

## 🚀 Cambios Principales v2.0

### ✅ Arquitectura Modular con API Routers
- **Separación por módulos**: El código ahora está organizado en routers independientes
- **Mantenibilidad**: Cada funcionalidad está en su propio archivo
- **Escalabilidad**: Fácil agregar nuevas funcionalidades sin tocar código existente

### 🔐 Autenticación JWT Profesional
- **Tokens JWT**: Sistema de autenticación moderno y seguro
- **Contraseñas hasheadas**: Bcrypt para seguridad de contraseñas
- **Compatibilidad**: Mantiene sistema de sesiones antiguo para transición gradual
- **API endpoints**: Autenticación por API para aplicaciones móviles/SPA futuras

### 📂 Nueva Estructura de Archivos

```
proyecto/
├── main.py                     # Aplicación principal (ahora limpia y modular)
├── auth.py                     # Sistema de autenticación JWT
├── db.py                       # Configuración de base de datos
├── requirements.txt            # Dependencias actualizadas
├── routers/                    # 📁 NUEVO: Módulo de routers
│   ├── __init__.py
│   ├── auth_router.py          # Login, register, JWT endpoints
│   ├── tests_router.py         # Tests vocacionales
│   ├── users_router.py         # Gestión de usuarios
│   ├── foro_router.py          # Foro de comentarios
│   └── programas_router.py     # Programas académicos
├── templates/                  # Plantillas HTML
├── static/                     # Archivos estáticos (CSS, JS, imágenes)
└── .env                        # Variables de entorno
```

## 🛠️ Instalación

### 1. Instalar dependencias actualizadas

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crear/actualizar archivo `.env`:

```env
# Base de datos (mantener igual)
URL_DATABASE=postgresql://postgres.nmhqudccjywubotnivgy:bsiPluov3Oi4vVQ0@aws-1-sa-east-1.pooler.supabase.com:5432/postgres

# Claves secretas (IMPORTANTE: cambiar en producción)
SECRET_KEY=tu-clave-secreta-para-sesiones-cambiar-en-produccion
JWT_SECRET_KEY=tu-clave-secreta-para-jwt-cambiar-en-produccion-12345

# Entorno
ENVIRONMENT=development  # En Vercel: production
```

### 3. Crear carpeta de routers

```bash
mkdir routers
touch routers/__init__.py
```

### 4. Copiar archivos de routers

Copiar todos los archivos `*_router.py` a la carpeta `routers/`:
- `auth_router.py`
- `tests_router.py`
- `users_router.py`
- `foro_router.py`
- `programas_router.py`

### 5. Actualizar archivo principal

Reemplazar `main.py` con la versión modular.

### 6. Agregar archivo de autenticación

Copiar `auth.py` a la raíz del proyecto.

### 7. Ejecutar migraciones de base de datos (si es necesario)

Si usas contraseñas antiguas sin hashear, puedes mantener la compatibilidad. El sistema detecta automáticamente si una contraseña está hasheada o no.

Para hashear contraseñas existentes (opcional):

```python
from auth import get_password_hash
from db import SessionLocal, text

db = SessionLocal()

# Obtener usuarios con contraseñas sin hashear
users = db.execute(text("SELECT id, contraseña FROM usuarios")).fetchall()

for user_id, pwd in users:
    if not pwd.startswith("$2b$"):  # No está hasheada
        hashed = get_password_hash(pwd)
        db.execute(
            text("UPDATE usuarios SET contraseña = :pwd WHERE id = :id"),
            {"pwd": hashed, "id": user_id}
        )

db.commit()
db.close()
```

## 🚀 Uso

### Iniciar servidor local

```bash
# Desarrollo (con auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O directamente
python main.py
```

### Acceder a la aplicación

- **Web**: http://localhost:8000
- **Docs API (Swagger)**: http://localhost:8000/docs
- **Docs API (ReDoc)**: http://localhost:8000/redoc

## 🔑 Nuevos Endpoints de Autenticación

### Login con JWT (API)

```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "usuario@ejemplo.com",
  "password": "contraseña"
}

# Respuesta:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nombre": "Usuario",
    "email": "usuario@ejemplo.com",
    "rol": "estudiante"
  }
}
```

### Registro con JWT (API)

```bash
POST /api/auth/register
Content-Type: application/json

{
  "nombre": "Nuevo Usuario",
  "email": "nuevo@ejemplo.com",
  "rol": "estudiante",
  "password": "contraseña123"
}
```

### Obtener información del usuario autenticado

```bash
GET /api/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Cambiar contraseña

```bash
POST /api/auth/change-password
Authorization: Bearer <token>
Content-Type: application/x-www-form-urlencoded

current_password=antigua&new_password=nueva&confirm_password=nueva
```

## 📝 Uso de Autenticación en Código

### Proteger endpoints con JWT

```python
from auth import get_current_user_jwt

@router.get("/api/privado")
async def endpoint_privado(
    current_user: dict = Depends(get_current_user_jwt)
):
    # El usuario está autenticado
    return {"message": f"Hola {current_user['nombre']}"}
```

### Autenticación opcional (híbrida)

```python
from auth import get_current_user_hybrid

@router.get("/publico-o-privado")
async def endpoint_flexible(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    # user puede ser None si no está autenticado
    if user:
        return {"message": f"Hola {user['nombre']}"}
    else:
        return {"message": "Acceso público"}
```

## 🔧 Despliegue en Vercel

### 1. Variables de entorno en Vercel

Agregar en el dashboard de Vercel:
- `URL_DATABASE`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `ENVIRONMENT=production`

### 2. Verificar vercel.json

El archivo ya está configurado correctamente para FastAPI.

### 3. Deploy

```bash
vercel --prod
```

## 📊 Ventajas del Nuevo Sistema

### Modularidad
- ✅ Código organizado por funcionalidad
- ✅ Fácil encontrar y modificar features
- ✅ Menos conflictos en trabajo en equipo

### Seguridad
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Tokens JWT con expiración
- ✅ Protección contra ataques de fuerza bruta
- ✅ Separación de autenticación y lógica de negocio

### Escalabilidad
- ✅ Agregar nuevos routers sin tocar main.py
- ✅ API lista para apps móviles
- ✅ Fácil implementar microservicios en futuro

### Compatibilidad
- ✅ Sistema de sesiones antiguo sigue funcionando
- ✅ Transición gradual sin romper funcionalidad
- ✅ Usuarios existentes pueden seguir usando la app

## 🐛 Troubleshooting

### Error: "No module named 'jose'"

```bash
pip install python-jose[cryptography]
```

### Error: "No module named 'passlib'"

```bash
pip install passlib[bcrypt]
```

### Error: "Cannot import name 'auth_router'"

Verificar que existe `routers/__init__.py` y todos los archivos de routers.

### Error en producción con sesiones

Verificar que `ENVIRONMENT=production` y `https_only=True` en SessionMiddleware.

## 📚 Recursos Adicionales

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **JWT.io**: https://jwt.io
- **SQLAlchemy**: https://docs.sqlalchemy.org
- **Bcrypt**: https://github.com/pyca/bcrypt/

## 👥 Contribución

Para agregar nuevas funcionalidades:

1. Crear nuevo router en `routers/mi_nuevo_router.py`
2. Importarlo en `main.py`
3. Incluirlo con `app.include_router(mi_nuevo_router.router)`

## 📄 Licencia

[Tu licencia aquí]

## 🙋 Soporte

Para dudas o problemas, contactar a [polarishelpco@gmail.com]