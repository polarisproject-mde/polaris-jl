# ========================================
# main.py - APLICACIÓN MODULAR CON ROUTERS
# ========================================

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import secrets
import os

# Importar configuración de base de datos
from db import get_db

# Importar sistema de autenticación
from auth import get_current_user_session, get_current_user_hybrid

# Importar todos los routers
from routers import auth_router, tests_router, users_router, foro_router, programas_router

# ================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ================================

app = FastAPI(
    title="Plataforma Vocacional",
    description="Sistema completo de orientación vocacional con tests, foro y recursos",
    version="2.0.0"
)

# Detectar entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production" or os.getenv("VERCEL") is not None

# ================================
# MIDDLEWARE DE SESIONES
# ================================

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600 * 24 * 7,  # 7 días
    same_site="none" if IS_PRODUCTION else "lax",
    https_only=IS_PRODUCTION,
    session_cookie="vocacional_session"
)

# ================================
# CONFIGURACIÓN DE TEMPLATES Y ESTÁTICOS
# ================================

templates = Jinja2Templates(directory="templates")

# Configurar archivos estáticos
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

print(f"📁 BASE_DIR: {BASE_DIR}")
print(f"📁 STATIC_DIR: {STATIC_DIR}")
print(f"📁 STATIC_DIR exists: {STATIC_DIR.exists()}")

if IS_PRODUCTION:
    try:
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
        print("✅ Modo PRODUCCIÓN - archivos estáticos montados")
    except Exception as e:
        print(f"⚠️ Error montando static en producción: {e}")
else:
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Modo DESARROLLO - archivos estáticos montados")
    except Exception as e:
        print(f"⚠️ Error montando static: {e}")

# ================================
# INCLUIR ROUTERS
# ================================

# Router de autenticación (login, register, JWT)
app.include_router(
    auth_router.router,
    tags=["Autenticación"]
)

# Router de tests vocacionales
app.include_router(
    tests_router.router,
    tags=["Tests Vocacionales"]
)

# Router de gestión de usuarios
app.include_router(
    users_router.router,
    tags=["Usuarios"]
)

# Router del foro de comentarios
app.include_router(
    foro_router.router,
    tags=["Foro"]
)

# Router de programas académicos
app.include_router(
    programas_router.router,
    tags=["Programas Académicos"]
)

# ================================
# RUTAS PRINCIPALES (PÁGINAS PÚBLICAS)
# ================================

@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    """Página de inicio"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/blog", response_class=HTMLResponse, name="blog")
async def blog(request: Request):
    """Blog de orientación vocacional"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("blog.html", {"request": request, "user": user})

@app.get("/carrerasdem", response_class=HTMLResponse, name="carrerasdem")
async def carrerasdem(request: Request):
    """Catálogo de carreras más demandadas"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("carrerasdem.html", {"request": request, "user": user})

@app.get("/comoelegir", response_class=HTMLResponse, name="comoelegir")
async def como_elegir(request: Request):
    """Guía: Cómo elegir carrera"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("comoelegir.html", {"request": request, "user": user})

@app.get("/errorescom", response_class=HTMLResponse, name="errorescom")
async def errores_comunes(request: Request):
    """Errores comunes al elegir carrera"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("errores.html", {"request": request, "user": user})

@app.get("/fechasimp", response_class=HTMLResponse, name="fechasimp")
async def fechas_importantes(request: Request):
    """Calendario de fechas importantes"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("fechasimp.html", {"request": request, "user": user})

@app.get("/guiav", response_class=HTMLResponse, name="guiav")
async def guia_vocacional(request: Request):
    """Guía vocacional completa"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("guiav.html", {"request": request, "user": user})

@app.get("/mitosyr", response_class=HTMLResponse, name="mitosyr")
async def mitos_y_realidades(request: Request):
    """Mitos y realidades sobre carreras"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("mitosyr.html", {"request": request, "user": user})

@app.get("/programas", response_class=HTMLResponse, name="programas-universidades")
async def programas(request: Request):
    """Programas universitarios"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("programas-universidades.html", {"request": request, "user": user})

@app.get("/recuryevent", response_class=HTMLResponse, name="recuryevent")
async def recursos_eventos(request: Request):
    """Recursos y eventos"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("recuryevent.html", {"request": request, "user": user})

@app.get("/articulos", response_class=HTMLResponse, name="articulos")
async def articulos(request: Request):
    """Artículos sobre orientación vocacional"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("articulos.html", {"request": request, "user": user})

@app.get("/webinars", response_class=HTMLResponse, name="webinars")
async def webinars(request: Request):
    """Webinars y charlas"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("webinars.html", {"request": request, "user": user})

@app.get("/becas", response_class=HTMLResponse, name="becas")
async def becas(request: Request):
    """Información sobre becas"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("becas.html", {"request": request, "user": user})

@app.get("/calculadora", response_class=HTMLResponse, name="calculadora")
async def calculadora(request: Request):
    """Calculadora de costos universitarios"""
    user = get_current_user_hybrid(request, next(get_db()))
    return templates.TemplateResponse("calculadora.html", {"request": request, "user": user})

# ================================
# ENDPOINTS DE DEBUG
# ================================

@app.get("/debug-static")
async def debug_static():
    """Endpoint de debugging para verificar archivos estáticos"""
    import os
    
    static_path = os.path.join(os.path.dirname(__file__), "static")
    css_path = os.path.join(static_path, "css")
    
    return {
        "environment": ENVIRONMENT,
        "is_production": IS_PRODUCTION,
        "static_exists": os.path.exists(static_path),
        "css_exists": os.path.exists(css_path),
        "static_files": os.listdir(static_path) if os.path.exists(static_path) else [],
        "css_files": os.listdir(css_path) if os.path.exists(css_path) else [],
        "current_dir": os.getcwd(),
        "dir_contents": os.listdir(os.getcwd())
    }

@app.get("/api/check-session")
async def check_session(request: Request):
    """Verifica si hay sesión activa"""
    user = get_current_user_session(request)
    return {
        "logged_in": user is not None,
        "user": user
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": "2.0.0"
    }

# ================================
# PUNTO DE ENTRADA
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )