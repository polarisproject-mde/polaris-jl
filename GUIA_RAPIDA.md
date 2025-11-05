# 🚀 Guía Rápida de Implementación

## ⚡ En 10 Minutos

### Paso 1: Preparar Entorno (2 min)

```bash
# 1. Crear backup
cp main.py main_backup.py
cp -r . ../backup_proyecto/

# 2. Crear carpeta de routers
mkdir routers
touch routers/__init__.py
```

### Paso 2: Instalar Dependencias (2 min)

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar nuevas dependencias JWT
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install bcrypt==4.2.1

# O instalar todo de una vez
pip install -r requirements.txt
```

### Paso 3: Copiar Archivos Nuevos (3 min)

**Archivos a crear:**

1. **Raíz del proyecto:**
   - `auth.py` (copiar contenido completo)

2. **Carpeta routers/:**
   - `auth_router.py`
   - `tests_router.py`
   - `users_router.py`
   - `foro_router.py`
   - `programas_router.py`

3. **Archivos auxiliares (opcionales):**
   - `migrate_passwords.py`
   - `restore_passwords.py`
   - `README.md`

### Paso 4: Reemplazar main.py (1 min)

```bash
# Hacer backup
mv main.py main_old.py

# Copiar nueva versión
cp main_new.py main.py
```

### Paso 5: Configurar Variables (1 min)

Agregar a `.env`:
```env
JWT_SECRET_KEY=cambiar-esto-en-produccion-usar-secreto-largo-y-aleatorio
```

### Paso 6: Probar (1 min)

```bash
# Iniciar servidor
python main.py

# O con uvicorn
uvicorn main:app --reload
```

Abrir navegador:
- http://localhost:8000
- http://localhost:8000/docs (Swagger UI)

---

## ✅ Verificación Rápida

### 1. Verificar Importaciones

```python
# Probar en terminal Python
python
>>> from auth import get_current_user_jwt
>>> from routers import auth_router
>>> print("✅ Todo OK")
```

### 2. Verificar Rutas

Abrir http://localhost:8000/docs y verificar:
- ✅ Sección "Autenticación" existe
- ✅ POST /api/auth/login existe
- ✅ GET /api/auth/me existe
- ✅ Todas las rutas anteriores siguen funcionando

### 3. Probar Login

**Login Tradicional:**
1. Ir a http://localhost:8000/login
2. Ingresar credenciales existentes
3. Debe redirigir a /
4. Debe mostrar usuario logueado

**Login JWT (con curl):**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"tu@email.com","password":"tucontraseña"}'
```

Debe retornar:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

---

## 🔧 Solución de Problemas Comunes

### Error: ModuleNotFoundError: No module named 'jose'

```bash
pip install python-jose[cryptography]
```

### Error: ModuleNotFoundError: No module named 'passlib'

```bash
pip install passlib[bcrypt]
```

### Error: Cannot import name 'auth_router'

**Verificar estructura:**
```
proyecto/
├── main.py
├── auth.py
├── routers/
│   ├── __init__.py  ← Este archivo DEBE existir
│   ├── auth_router.py
│   ├── tests_router.py
│   └── ...
```

**Solución:**
```bash
touch routers/__init__.py
```

### Error: ImportError en auth.py

**Causa:** Importaciones circulares con main.py

**Solución:** Mover `TESTS_CONFIG` y funciones de tests a archivo separado o mantenerlas en main.py

### Login no funciona después de cambios

**Opción 1: Sistema híbrido (mantiene compatibilidad)**
- Las contraseñas antiguas siguen funcionando
- auth.py detecta automáticamente si están hasheadas

**Opción 2: Migrar todo a bcrypt**
```bash
python migrate_passwords.py
```

---

## 📱 Uso de la API JWT

### 1. Obtener Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
  }'
```

Respuesta:
```json
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

### 2. Usar Token en Requests

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Obtener info del usuario
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Obtener dimensiones vocacionales
curl -X GET http://localhost:8000/api/usuario/dimensiones \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Probar con Postman

1. Crear request POST a `/api/auth/login`
2. Body → raw → JSON:
   ```json
   {
     "email": "tu@email.com",
     "password": "tucontraseña"
   }
   ```
3. Enviar y copiar `access_token`
4. En siguiente request:
   - Headers → Authorization: `Bearer {token}`

---

## 🔐 Migrar Contraseñas (Opcional)

### ¿Cuándo hacerlo?
- Después de verificar que todo funciona
- En horario de bajo tráfico
- Con backup de base de datos

### Proceso

```bash
# 1. Ejecutar script de migración
python migrate_passwords.py

# 2. Revisar reporte
# El script muestra:
# - Contraseñas migradas
# - Errores (si hay)
# - Backup creado

# 3. Confirmar cuando se solicite
# Si/no

# 4. Verificar que todo funciona
python main.py
```

### Si algo sale mal

```bash
# Restaurar contraseñas
python restore_passwords.py
```

---

## 📊 Checklist Final

### Antes de Deploy a Producción

- [ ] Todo funciona en local
- [ ] Tests pasan correctamente
- [ ] Login tradicional funciona
- [ ] Login JWT funciona
- [ ] Swagger accesible en /docs
- [ ] Variables de entorno configuradas
- [ ] Backup de base de datos hecho
- [ ] Backup de código hecho

### Variables de Entorno en Producción

```env
# Vercel / Render / Railway
URL_DATABASE=postgresql://...
SECRET_KEY=genera-clave-secreta-larga-y-aleatoria-123
JWT_SECRET_KEY=otra-clave-diferente-tambien-aleatoria-456
ENVIRONMENT=production
```

**⚠️ IMPORTANTE:** Generar claves seguras:

```python
import secrets
print(secrets.token_hex(32))  # Para SECRET_KEY
print(secrets.token_hex(32))  # Para JWT_SECRET_KEY
```

### Deploy

```bash
# Vercel
vercel --prod

# O Git push si tienes auto-deploy
git add .
git commit -m "feat: implementar arquitectura modular con JWT"
git push origin main
```

---

## 🎯 Próximos Pasos Sugeridos

### Mejoras a Corto Plazo

1. **Mover TESTS_CONFIG a archivo separado**
   ```python
   # config/tests_config.py
   TESTS_CONFIG = {...}
   
   # main.py
   from config.tests_config import TESTS_CONFIG
   ```

2. **Agregar rate limiting**
   ```bash
   pip install slowapi
   ```

3. **Implementar refresh tokens**
   - Tokens de acceso: 15 min
   - Tokens de refresco: 7 días

### Mejoras a Mediano Plazo

1. **Testing automatizado**
   - pytest para unit tests
   - pytest-asyncio para tests async

2. **Documentación de API mejorada**
   - Agregar ejemplos a Swagger
   - Documentar modelos Pydantic

3. **Logging estructurado**
   - python-json-logger
   - Integración con servicios de monitoreo

### Mejoras a Largo Plazo

1. **App móvil**
   - Ya tienes API JWT lista
   - Flutter / React Native

2. **Microservicios**
   - Separar tests en servicio independiente
   - Separar autenticación

3. **Cache**
   - Redis para sesiones
   - Cache de resultados de tests

---

## 💡 Consejos Pro

1. **Usa el sistema híbrido inicialmente**
   - No fuerces a todos a migrar de inmediato
   - JWT + sesiones funcionan en paralelo

2. **Monitorea errores de autenticación**
   - Implementa logging detallado
   - Alerta si muchos fallos de login

3. **Documenta endpoints personalizados**
   - Swagger auto-documenta
   - Agrega descripciones a cada ruta

4. **Versiona tu API**
   ```python
   # Para futuro
   app.include_router(auth_router.router, prefix="/api/v1")
   ```

5. **Implementa CORS correctamente**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://tu-frontend.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## 🆘 Soporte

Si tienes problemas:

1. Revisa logs: `python main.py` muestra errores detallados
2. Verifica estructura de carpetas
3. Confirma que todas las dependencias están instaladas
4. Revisa variables de entorno
5. Consulta README.md para documentación completa

**¡Éxito con tu migración! 🚀**