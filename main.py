# ========================================
# INICIO DE main.py - SECCIÓN LIMPIA
# ========================================

from fastapi import FastAPI, Request, Depends, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional, List
from starlette.middleware.sessions import SessionMiddleware
import secrets
from pydantic import BaseModel
from datetime import datetime
import random
import json
from typing import Dict, List, Tuple
import os

from db import get_db

app = FastAPI()

# Detectar si estamos en producción (Vercel)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production" or os.getenv("VERCEL") is not None

# CRÍTICO: SessionMiddleware DEBE ir ANTES de app.mount()
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600 * 24 * 7,
    same_site="none" if IS_PRODUCTION else "lax",
    https_only=IS_PRODUCTION,
    session_cookie="vocacional_session"
)

# Configuración de templates
templates = Jinja2Templates(directory="templates")

# 🔥 CONFIGURACIÓN ARCHIVOS ESTÁTICOS - FIX DEFINITIVO PARA VERCEL
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

print(f"🔍 BASE_DIR: {BASE_DIR}")
print(f"🔍 STATIC_DIR: {STATIC_DIR}")
print(f"🔍 STATIC_DIR exists: {STATIC_DIR.exists()}")

if IS_PRODUCTION:
    # En Vercel, montar StaticFiles CON configuración especial
    try:
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
        print("✅ Modo PRODUCCIÓN - archivos estáticos montados")
    except Exception as e:
        print(f"⚠️ Error montando static en producción: {e}")
else:
    # En desarrollo local
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Modo DESARROLLO - archivos estáticos montados")
    except Exception as e:
        print(f"⚠️ Error montando static: {e}")


# ================================
# RUTA DE DEBUG PARA ARCHIVOS ESTÁTICOS
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

# ================================
# DEPENDENCIA DE AUTENTICACIÓN
# ================================

def get_current_user(request: Request) -> Optional[dict]:
    """
    Obtiene el usuario actual de la sesión.
    Retorna None si no hay usuario autenticado.
    """
    # Debug en producción
    if IS_PRODUCTION:
        print(f"Session keys: {list(request.session.keys())}")
        print(f"Logged in: {request.session.get('logged_in')}")
    
    user_id = request.session.get("user_id")
    
    if not user_id:
        return None
    
    return {
        "id": user_id,
        "nombre": request.session.get("user_nombre"),
        "gmail": request.session.get("user_gmail"),
        "rol": request.session.get("user_rol")
    }

TESTS_CONFIG = {
    "general": {
        "titulo": "Test Vocacional General",
        "descripcion": "Descubre tus áreas de interés profesional",
        "instrucciones": "Responde honestamente cada pregunta. No hay respuestas correctas o incorrectas.",
        "preguntas": [
            {"id": 1, "texto": "¿Disfrutas resolver problemas matemáticos y lógicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 2, "texto": "¿Te interesa comprender cómo funcionan las cosas y los fenómenos naturales?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 3, "texto": "¿Disfrutas trabajar con tecnología y computadoras?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 4, "texto": "¿Te gusta diseñar, construir o crear cosas nuevas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 5, "texto": "¿Te interesa el mundo de los negocios y las finanzas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 6, "texto": "¿Disfrutas realizar experimentos científicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 7, "texto": "¿Te gusta analizar datos y estadísticas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 8, "texto": "¿Te interesa entender cómo funcionan los mercados económicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 9, "texto": "¿Disfrutas programar o aprender lenguajes de programación?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 10, "texto": "¿Te gusta trabajar en proyectos de construcción o mecánicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 11, "texto": "¿Te interesa la innovación y las nuevas tecnologías?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 12, "texto": "¿Disfrutas gestionar proyectos y organizar recursos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 13, "texto": "¿Te gusta estudiar organismos vivos y ecosistemas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 14, "texto": "¿Te interesa optimizar procesos y mejorar la eficiencia?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 15, "texto": "¿Disfrutas aprender sobre química y reacciones químicas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 16, "texto": "¿Te gusta trabajar con circuitos y sistemas eléctricos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 17, "texto": "¿Te interesa el marketing y las estrategias de ventas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 18, "texto": "¿Disfrutas desarrollar aplicaciones o software?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 19, "texto": "¿Te gusta analizar problemas complejos y encontrar soluciones creativas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 20, "texto": "¿Te interesa la gestión financiera y las inversiones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 21, "texto": "¿Disfrutas trabajar en laboratorios y realizar investigaciones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 22, "texto": "¿Te gusta diseñar estructuras y planificar infraestructuras?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 23, "texto": "¿Te interesa la inteligencia artificial y el machine learning?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 24, "texto": "¿Disfrutas liderar equipos y tomar decisiones estratégicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 25, "texto": "¿Te gusta trabajar con física y entender las leyes del universo?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 26, "texto": "¿Te interesa la automatización y robótica?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 27, "texto": "¿Disfrutas analizar balances financieros y contabilidad?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 28, "texto": "¿Te gusta la biotecnología y la genética?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 29, "texto": "¿Te interesa la ciberseguridad y protección de sistemas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 30, "texto": "¿Disfrutas trabajar en la optimización de producción industrial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 31, "texto": "¿Te gusta emprender y crear tu propio negocio?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 32, "texto": "¿Te interesa el medio ambiente y la sostenibilidad?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 33, "texto": "¿Disfrutas diseñar interfaces y experiencias de usuario?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 34, "texto": "¿Te gusta analizar el comportamiento del consumidor?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 35, "texto": "¿Te interesa trabajar con energías renovables?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 36, "texto": "¿Disfrutas trabajar con bases de datos y gestión de información?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 37, "texto": "¿Te gusta investigar nuevos materiales y sus propiedades?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 38, "texto": "¿Te interesa la logística y cadena de suministro?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 39, "texto": "¿Disfrutas desarrollar videojuegos o aplicaciones interactivas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 40, "texto": "¿Te gusta analizar tendencias económicas y hacer proyecciones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]}
        ]
    },
    
    "tecnologia": {
        "titulo": "Test de Tecnología",
        "descripcion": "Evalúa tu afinidad con carreras tecnológicas",
        "instrucciones": "Este test te ayudará a identificar si las carreras tecnológicas son para ti.",
        "preguntas": [
            {"id": 1, "texto": "¿Te interesa aprender lenguajes de programación?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 2, "texto": "¿Disfrutas resolver problemas usando lógica y algoritmos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 3, "texto": "¿Te gusta estar al día con las últimas tecnologías?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 4, "texto": "¿Disfrutas diseñar y desarrollar aplicaciones o sitios web?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 5, "texto": "¿Te interesa la inteligencia artificial y el aprendizaje automático?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 6, "texto": "¿Disfrutas trabajar con bases de datos y gestión de información?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 7, "texto": "¿Te gusta la ciberseguridad y proteger sistemas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 8, "texto": "¿Te interesa desarrollar videojuegos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 9, "texto": "¿Disfrutas configurar y administrar redes de computadoras?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 10, "texto": "¿Te gusta analizar y visualizar grandes volúmenes de datos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 11, "texto": "¿Te interesa el cloud computing y servicios en la nube?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 12, "texto": "¿Disfrutas automatizar tareas usando scripts o programas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 13, "texto": "¿Te gusta diseñar interfaces de usuario atractivas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 14, "texto": "¿Te interesa el desarrollo móvil (apps para celulares)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 15, "texto": "¿Disfrutas debuggear (encontrar y corregir errores) en código?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 16, "texto": "¿Te gusta trabajar con hardware y componentes de computadoras?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 17, "texto": "¿Te interesa el Internet de las Cosas (IoT)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 18, "texto": "¿Disfrutas optimizar el rendimiento de aplicaciones?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 19, "texto": "¿Te gusta la realidad virtual y aumentada?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 20, "texto": "¿Te interesa el blockchain y las criptomonedas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 21, "texto": "¿Disfrutas participar en hackathons o competencias de programación?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 22, "texto": "¿Te gusta trabajar con APIs y servicios web?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 23, "texto": "¿Te interesa DevOps y la integración continua?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 24, "texto": "¿Disfrutas aprender nuevos frameworks y librerías?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 25, "texto": "¿Te gusta el desarrollo backend (servidor)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 26, "texto": "¿Te interesa el testing y aseguramiento de calidad?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 27, "texto": "¿Disfrutas el trabajo colaborativo con control de versiones (Git)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 28, "texto": "¿Te gusta crear soluciones innovadoras con tecnología?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 29, "texto": "¿Te interesa la arquitectura de software?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 30, "texto": "¿Disfrutas mantenerte actualizado con tendencias tecnológicas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]}
        ]
    },
    
    "ciencias": {
        "titulo": "Test de Ciencias",
        "descripcion": "Descubre tu vocación científica",
        "instrucciones": "Responde según tu interés real en actividades científicas.",
        "preguntas": [
            {"id": 1, "texto": "¿Te gusta realizar experimentos y descubrir cómo funcionan las cosas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 2, "texto": "¿Te interesa estudiar organismos vivos y ecosistemas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 3, "texto": "¿Disfrutas trabajar en laboratorios?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 4, "texto": "¿Te gusta la química y las reacciones químicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 5, "texto": "¿Te interesa la física y las leyes del universo?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 6, "texto": "¿Disfrutas investigar y formular hipótesis?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 7, "texto": "¿Te gusta la biotecnología y la genética?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 8, "texto": "¿Te interesa la astronomía y el espacio?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 9, "texto": "¿Disfrutas analizar datos experimentales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 10, "texto": "¿Te gusta la medicina y ayudar a la salud de las personas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 11, "texto": "¿Te interesa la ecología y conservación ambiental?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 12, "texto": "¿Disfrutas usar el método científico para resolver problemas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 13, "texto": "¿Te gusta la microbiología y el estudio de microorganismos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 14, "texto": "¿Te interesa la neurociencia y el cerebro humano?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 15, "texto": "¿Disfrutas investigar sobre materiales y sus propiedades?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 16, "texto": "¿Te gusta la farmacología y el desarrollo de medicamentos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 17, "texto": "¿Te interesa la geología y el estudio de la Tierra?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 18, "texto": "¿Disfrutas estudiar el comportamiento animal?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 19, "texto": "¿Te gusta la bioquímica y procesos moleculares?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 20, "texto": "¿Te interesa la climatología y cambio climático?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 21, "texto": "¿Disfrutas la investigación en laboratorio por largas horas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 22, "texto": "¿Te gusta leer artículos científicos y papers?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 23, "texto": "¿Te interesa la nanotecnología?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 24, "texto": "¿Disfrutas usar microscopios y equipos especializados?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 25, "texto": "¿Te gusta contribuir al avance del conocimiento científico?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 26, "texto": "¿Te interesa la oceanografía y vida marina?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 27, "texto": "¿Disfrutas analizar muestras y hacer mediciones precisas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 28, "texto": "¿Te gusta la paleontología y el estudio de fósiles?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 29, "texto": "¿Te interesa la toxicología y sustancias químicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 30, "texto": "¿Disfrutas participar en proyectos de investigación científica?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]}
        ]
    },
    
    "ingenieria": {
        "titulo": "Test de Ingeniería",
        "descripcion": "Evalúa tu aptitud para carreras de ingeniería",
        "instrucciones": "Este test mide tu afinidad con el pensamiento ingenieril.",
        "preguntas": [
            {"id": 1, "texto": "¿Disfrutas diseñar y construir cosas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 2, "texto": "¿Te gusta resolver problemas técnicos complejos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 3, "texto": "¿Te interesa el diseño de estructuras y edificaciones?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 4, "texto": "¿Disfrutas trabajar con máquinas y mecanismos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 5, "texto": "¿Te gusta la electricidad y los circuitos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 6, "texto": "¿Te interesa optimizar procesos industriales?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 7, "texto": "¿Disfrutas usar herramientas de diseño CAD?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 8, "texto": "¿Te gusta la robótica y automatización?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 9, "texto": "¿Te interesa la ingeniería ambiental y sostenibilidad?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 10, "texto": "¿Disfrutas calcular y hacer cálculos técnicos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 11, "texto": "¿Te gusta trabajar con materiales y sus propiedades?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 12, "texto": "¿Te interesa la gestión de proyectos de ingeniería?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 13, "texto": "¿Disfrutas hacer prototipos y pruebas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 14, "texto": "¿Te gusta la termodinámica y transferencia de calor?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 15, "texto": "¿Te interesa el control de calidad en manufactura?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 16, "texto": "¿Disfrutas diseñar sistemas de producción?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 17, "texto": "¿Te gusta la mecánica de fluidos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 18, "texto": "¿Te interesa el diseño de vehículos y transporte?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 19, "texto": "¿Disfrutas trabajar con energías renovables?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 20, "texto": "¿Te gusta el análisis estructural?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 21, "texto": "¿Te interesa la construcción de infraestructura?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 22, "texto": "¿Disfrutas hacer simulaciones y modelado?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 23, "texto": "¿Te gusta la ingeniería biomédica?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 24, "texto": "¿Te interesa el tratamiento de aguas y residuos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 25, "texto": "¿Disfrutas innovar y mejorar diseños existentes?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 26, "texto": "¿Te gusta la logística y cadena de suministro?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 27, "texto": "¿Te interesa el diseño de sistemas de telecomunicaciones?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 28, "texto": "¿Disfrutas trabajar en proyectos multidisciplinarios?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 29, "texto": "¿Te gusta resolver problemas de ingeniería en campo?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 30, "texto": "¿Te interesa contribuir al desarrollo tecnológico?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]}
        ]
    },
    
    "economia": {
        "titulo": "Test de Economía",
        "descripcion": "Descubre tu afinidad con carreras económicas y de negocios",
        "instrucciones": "Responde según tu interés en temas económicos y financieros.",
        "preguntas": [
            {"id": 1, "texto": "¿Te interesa entender cómo funcionan los mercados y las finanzas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 2, "texto": "¿Disfrutas analizar datos financieros y balances?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 3, "texto": "¿Te gusta gestionar negocios y organizaciones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 4, "texto": "¿Te interesa el marketing y estrategias de ventas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 5, "texto": "¿Disfrutas hacer inversiones y análisis de riesgo?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 6, "texto": "¿Te gusta emprender y crear negocios propios?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 7, "texto": "¿Te interesa la contabilidad y registros financieros?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 8, "texto": "¿Disfrutas negociar y cerrar acuerdos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 9, "texto": "¿Te gusta liderar equipos y tomar decisiones empresariales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 10, "texto": "¿Te interesa el comercio internacional?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 11, "texto": "¿Disfrutas analizar el comportamiento del consumidor?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 12, "texto": "¿Te gusta gestionar recursos humanos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 13, "texto": "¿Te interesa la banca y servicios financieros?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 14, "texto": "¿Disfrutas hacer proyecciones y planificación estratégica?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 15, "texto": "¿Te gusta la economía global y políticas económicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 16, "texto": "¿Te interesa la consultoría empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 17, "texto": "¿Disfrutas trabajar con presupuestos y planeación financiera?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 18, "texto": "¿Te gusta el análisis de mercados y competencia?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 19, "texto": "¿Te interesa la gestión de proyectos empresariales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 20, "texto": "¿Disfrutas leer sobre finanzas y economía?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 21, "texto": "¿Te gusta el e-commerce y negocios digitales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 22, "texto": "¿Te interesa la auditoría y control interno?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 23, "texto": "¿Disfrutas optimizar costos y mejorar rentabilidad?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 24, "texto": "¿Te gusta la gestión de la calidad empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 25, "texto": "¿Te interesa la responsabilidad social empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 26, "texto": "¿Disfrutas trabajar con indicadores de desempeño (KPIs)?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 27, "texto": "¿Te gusta la gestión de marcas y branding?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 28, "texto": "¿Te interesa el análisis económico y estadístico?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 29, "texto": "¿Disfrutas asistir a eventos de networking empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 30, "texto": "¿Te gusta tomar decisiones basadas en datos financieros?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]}
        ]
    }
}

# ===================================
# INSTRUCCIONES PARA AGREGAR MÁS PREGUNTAS:
# ===================================
# 
# Para agregar más preguntas a cualquier test, simplemente copia el formato:
#
# {"id": NUMERO, "texto": "TU PREGUNTA AQUÍ",
#  "opciones": [
#      {"valor": "A", "texto": "Opción más positiva"}, 
#      {"valor": "B", "texto": "Opción positiva"}, 
#      {"valor": "C", "texto": "Opción neutral"}, 
#      {"valor": "D", "texto": "Opción negativa"}, 
#      {"valor": "E", "texto": "Opción más negativa"}
#  ]},
#
# IMPORTANTE:
# - El "id" debe ser consecutivo (1, 2, 3, 4...)
# - Mantén siempre 5 opciones (A, B, C, D, E)
# - A = más positivo/mayor acuerdo (5 puntos)
# - E = más negativo/mayor desacuerdo (1 punto)
# - No olvides la coma al final de cada pregunta (excepto la última)
#

# ================================
# SISTEMA DE PUNTUACIÓN Y PERFILES
# ================================

# Sistema de puntuación: A=5, B=4, C=3, D=2, E=1
PUNTUACION_VALORES = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

# ================================
# MAPEO COMPLETO Y BALANCEADO (40 PREGUNTAS)
# ================================

MAPEO_PREGUNTAS_GENERAL = {
    # === BLOQUE 1: MATEMÁTICAS & LÓGICA ===
    1: {"matematicas": 1.0, "logica": 0.9, "analitico": 0.7, "resolucion": 0.6},
    7: {"analitico": 1.0, "datos": 0.9, "matematicas": 0.7, "estadistica": 0.6},
    19: {"analitico": 1.0, "resolucion": 1.0, "logica": 0.8, "creatividad": 0.7},
    
    # === BLOQUE 2: CIENCIAS NATURALES ===
    2: {"ciencias": 1.0, "curiosidad": 0.8, "investigacion": 0.7, "naturaleza": 0.5},
    6: {"ciencias": 1.0, "investigacion": 1.0, "metodico": 0.8, "laboratorio": 0.7},
    13: {"biologia": 1.0, "ciencias": 0.9, "naturaleza": 0.8, "ecologia": 0.6},
    15: {"quimica": 1.0, "ciencias": 0.9, "laboratorio": 0.8, "investigacion": 0.6},
    21: {"investigacion": 1.0, "ciencias": 0.9, "paciencia": 0.7, "metodico": 0.7},
    25: {"fisica": 1.0, "ciencias": 0.9, "teorico": 0.8, "matematicas": 0.7},
    28: {"biotecnologia": 1.0, "biologia": 0.8, "ciencias": 0.8, "innovacion": 0.6},
    
    # === BLOQUE 3: TECNOLOGÍA & PROGRAMACIÓN ===
    3: {"tecnologia": 1.0, "practico": 0.7, "digital": 0.8},
    9: {"programacion": 1.0, "tecnologia": 0.9, "logica": 0.8, "algoritmos": 0.7},
    11: {"innovacion": 1.0, "tecnologia": 0.9, "futuro": 0.8, "tendencias": 0.6},
    18: {"programacion": 1.0, "desarrollo": 1.0, "tecnologia": 0.9, "creatividad": 0.5},
    23: {"ia": 1.0, "tecnologia": 0.9, "programacion": 0.8, "matematicas": 0.7},
    29: {"seguridad": 1.0, "tecnologia": 0.9, "proteccion": 0.8, "sistemas": 0.7},
    33: {"ux": 1.0, "diseno": 0.9, "tecnologia": 0.8, "creatividad": 0.8, "usuario": 0.7},
    36: {"datos": 1.0, "tecnologia": 0.9, "organizacion": 0.8, "analitico": 0.7},
    39: {"gaming": 1.0, "programacion": 0.9, "creatividad": 0.9, "tecnologia": 0.8},
    
    # === BLOQUE 4: INGENIERÍA & CONSTRUCCIÓN ===
    4: {"diseno": 1.0, "creatividad": 0.9, "ingenieria": 0.7, "construccion": 0.6},
    10: {"construccion": 1.0, "ingenieria": 0.9, "practico": 0.9, "mecanico": 0.7},
    14: {"optimizacion": 1.0, "ingenieria": 0.8, "analitico": 0.7, "eficiencia": 0.8},
    16: {"electrica": 1.0, "ingenieria": 0.9, "tecnico": 0.9, "sistemas": 0.7},
    22: {"civil": 1.0, "ingenieria": 0.9, "diseno": 0.8, "construccion": 0.7, "estructural": 0.8},
    26: {"automatizacion": 1.0, "robotica": 0.9, "ingenieria": 0.8, "tecnologia": 0.7},
    30: {"industrial": 1.0, "ingenieria": 0.9, "produccion": 0.9, "optimizacion": 0.7},
    35: {"energia": 1.0, "renovables": 0.9, "ingenieria": 0.8, "ambiental": 0.7, "sostenibilidad": 0.8},
    37: {"materiales": 1.0, "ciencias": 0.8, "investigacion": 0.8, "innovacion": 0.6},
    
    # === BLOQUE 5: NEGOCIOS & ECONOMÍA ===
    5: {"negocios": 1.0, "finanzas": 0.8, "estrategia": 0.7, "empresarial": 0.6},
    8: {"economia": 1.0, "mercados": 0.9, "negocios": 0.8, "analitico": 0.6},
    12: {"liderazgo": 1.0, "gestion": 0.9, "organizacion": 0.9, "negocios": 0.6},
    17: {"marketing": 1.0, "comunicacion": 0.9, "negocios": 0.8, "creatividad": 0.7, "ventas": 0.8},
    20: {"finanzas": 1.0, "inversion": 0.9, "negocios": 0.8, "analitico": 0.7, "riesgo": 0.6},
    24: {"liderazgo": 1.0, "decision": 0.9, "estrategia": 0.8, "negocios": 0.7},
    27: {"contabilidad": 1.0, "finanzas": 0.8, "detalle": 0.9, "negocios": 0.7, "numeros": 0.8},
    31: {"emprendimiento": 1.0, "negocios": 0.9, "innovacion": 0.8, "riesgo": 0.7, "liderazgo": 0.6},
    34: {"consumidor": 1.0, "marketing": 0.9, "psicologia": 0.7, "negocios": 0.6, "investigacion": 0.5},
    38: {"logistica": 1.0, "cadena": 0.9, "organizacion": 0.8, "optimizacion": 0.7, "negocios": 0.6},
    40: {"economia": 1.0, "proyeccion": 0.9, "analitico": 0.8, "tendencias": 0.7, "finanzas": 0.6},
    
    # === BLOQUE 6: SOSTENIBILIDAD & MEDIO AMBIENTE ===
    32: {"ambiental": 1.0, "sostenibilidad": 1.0, "responsabilidad": 0.9, "ecologia": 0.8, "futuro": 0.6},
}

# ================================
# PERFILES VOCACIONALES MEJORADOS
# ================================

PERFILES_DETALLADOS = {
    "desarrollador_software": {
        "nombre": "Desarrollador/a de Software",
        "indicadores_clave": {
            "tecnologia": (72, 100),      # ✅ Cambiado de 70
            "programacion": (75, 100),    # Igual
            "logica": (70, 100),          # Igual
        },
        "indicadores_secundarios": {
            "analitico": (65, 100),       # ✅ Cambiado de 60
            "resolucion": (65, 100),      # Igual
            "creatividad": (50, 100),
        },
        "carreras": [
            {
                "nombre": "Ingeniería de Software",
                "match_base": 95,
                "factores": {
                    "programacion": 0.35,
                    "tecnologia": 0.30,
                    "logica": 0.20,
                    "creatividad": 0.15
                }
            },
            {
                "nombre": "Ingeniería de Sistemas",
                "match_base": 92,
                "factores": {
                    "tecnologia": 0.35,
                    "programacion": 0.30,
                    "analitico": 0.20,
                    "organizacion": 0.15
                }
            },
            {
                "nombre": "Ciencia de Datos",
                "match_base": 88,
                "factores": {
                    "datos": 0.35,
                    "programacion": 0.30,
                    "analitico": 0.25,
                    "matematicas": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil muestra una fuerte inclinación hacia el desarrollo de software. Destacas en pensamiento lógico, resolución de problemas y tienes la creatividad necesaria para diseñar soluciones innovadoras.",
        "fortalezas_especificas": [
            "Pensamiento algorítmico y estructurado",
            "Capacidad de abstracción de problemas complejos",
            "Aprendizaje continuo de nuevas tecnologías",
            "Creatividad aplicada a soluciones técnicas"
        ],
        "areas_desarrollo": [
            "Comunicación técnica con equipos no técnicos",
            "Gestión de proyectos y plazos",
            "Habilidades de presentación",
            "Trabajo colaborativo en equipos grandes"
        ],
        "campo_laboral": [
            "Empresas de tecnología (startups y corporaciones)",
            "Desarrollo de aplicaciones móviles y web",
            "Consultoría tecnológica",
            "Investigación y desarrollo (I+D)",
            "Trabajo remoto/freelance con proyectos globales"
        ]
    },
    
    "cientifico_investigador": {
        "nombre": "Científico/a Investigador/a",
        "indicadores_clave": {
            "ciencias": (75, 100),        # Igual
            "investigacion": (75, 100),   # Igual
            "metodico": (68, 100),
        },
        "indicadores_secundarios": {
            "curiosidad": (65, 100),      # ✅ Cambiado de 70
            "paciencia": (60, 100),       # ✅ Cambiado de 65
            "laboratorio": (55, 100),
        },
        "carreras": [
            {
                "nombre": "Biología",
                "match_base": 90,
                "factores": {
                    "biologia": 0.40,
                    "investigacion": 0.30,
                    "naturaleza": 0.20,
                    "metodico": 0.10
                }
            },
            {
                "nombre": "Química",
                "match_base": 88,
                "factores": {
                    "quimica": 0.40,
                    "laboratorio": 0.25,
                    "investigacion": 0.25,
                    "analitico": 0.10
                }
            },
            {
                "nombre": "Biotecnología",
                "match_base": 92,
                "factores": {
                    "biotecnologia": 0.35,
                    "biologia": 0.25,
                    "innovacion": 0.20,
                    "investigacion": 0.20
                }
            }
        ],
        "descripcion": "Tienes un perfil científico sólido con gran curiosidad intelectual. Te apasiona entender cómo funciona el mundo natural y tienes la disciplina necesaria para la investigación rigurosa.",
        "fortalezas_especificas": [
            "Método científico riguroso",
            "Pensamiento crítico y analítico",
            "Atención meticulosa al detalle",
            "Capacidad para trabajo experimental sistemático"
        ],
        "areas_desarrollo": [
            "Aplicación comercial de investigaciones",
            "Comunicación científica para público general",
            "Gestión de financiamiento y grants",
            "Networking en comunidad científica"
        ],
        "campo_laboral": [
            "Universidades e institutos de investigación",
            "Laboratorios farmacéuticos",
            "Centros de biotecnología",
            "Organizaciones ambientales",
            "Docencia e investigación académica"
        ]
    },
    
    "ingeniero_constructor": {
        "nombre": "Ingeniero/a de Construcción e Infraestructura",
        "indicadores_clave": {
            "ingenieria": (70, 100),
            "practico": (70, 100),
            "diseno": (65, 100)
        },
        "indicadores_secundarios": {
            "matematicas": (62, 100),
            "organizacion": (60, 100),
            "construccion": (65, 100)
        },
        "carreras": [
            {
                "nombre": "Ingeniería Civil",
                "match_base": 95,
                "factores": {
                    "civil": 0.40,
                    "construccion": 0.25,
                    "diseno": 0.20,
                    "matematicas": 0.15
                }
            },
            {
                "nombre": "Ingeniería Mecánica",
                "match_base": 90,
                "factores": {
                    "ingenieria": 0.35,
                    "practico": 0.30,
                    "diseno": 0.20,
                    "tecnico": 0.15
                }
            },
            {
                "nombre": "Arquitectura",
                "match_base": 85,
                "factores": {
                    "diseno": 0.40,
                    "creatividad": 0.25,
                    "construccion": 0.20,
                    "estetico": 0.15
                }
            }
        ],
        "descripcion": "Tu perfil indica una fuerte vocación por crear infraestructura y soluciones tangibles. Combinas habilidades técnicas con visión espacial y capacidad de materializar proyectos.",
        "fortalezas_especificas": [
            "Pensamiento espacial y visual desarrollado",
            "Capacidad de planificación a gran escala",
            "Comprensión de sistemas físicos complejos",
            "Enfoque práctico orientado a resultados"
        ],
        "areas_desarrollo": [
            "Herramientas digitales avanzadas (BIM, CAD 3D)",
            "Sostenibilidad y construcción verde",
            "Gestión de equipos multidisciplinarios",
            "Innovación en materiales"
        ],
        "campo_laboral": [
            "Empresas constructoras",
            "Consultoras de ingeniería",
            "Sector público (infraestructura)",
            "Desarrollo inmobiliario",
            "Consultoría independiente"
        ]
    },
    
    "estratega_negocios": {
        "nombre": "Estratega de Negocios",
        "indicadores_clave": {
            "negocios": (72, 100),
            "estrategia": (70, 100),
            "analitico": (65, 100)
        },
        "indicadores_secundarios": {
            "liderazgo": (62, 100),
            "decision": (65, 100),
            "comunicacion": (60, 100)
        },
        "carreras": [
            {
                "nombre": "Administración de Empresas",
                "match_base": 93,
                "factores": {
                    "negocios": 0.35,
                    "liderazgo": 0.25,
                    "organizacion": 0.20,
                    "estrategia": 0.20
                }
            },
            {
                "nombre": "Economía",
                "match_base": 90,
                "factores": {
                    "economia": 0.40,
                    "analitico": 0.30,
                    "proyeccion": 0.20,
                    "matematicas": 0.10
                }
            },
            {
                "nombre": "Finanzas",
                "match_base": 91,
                "factores": {
                    "finanzas": 0.40,
                    "analitico": 0.30,
                    "inversion": 0.20,
                    "riesgo": 0.10
                }
            }
        ],
        "descripcion": "Tienes un perfil orientado al mundo empresarial con fuerte capacidad analítica. Destacas en pensamiento estratégico y toma de decisiones basadas en datos.",
        "fortalezas_especificas": [
            "Visión estratégica de negocios",
            "Análisis cuantitativo y financiero",
            "Toma de decisiones bajo incertidumbre",
            "Comprensión de dinámicas de mercado"
        ],
        "areas_desarrollo": [
            "Habilidades técnicas (programación básica, BI)",
            "Innovación disruptiva y digital",
            "Gestión del cambio organizacional",
            "Pensamiento de diseño (design thinking)"
        ],
        "campo_laboral": [
            "Consultoría estratégica",
            "Banca de inversión",
            "Empresas corporativas (estrategia, finanzas)",
            "Startups (como CFO o estratega)",
            "Analista financiero"
        ]
    },
    
    "innovador_tecnologico": {
        "nombre": "Innovador/a Tecnológico/a",
        "indicadores_clave": {
            "tecnologia": (70, 100),
            "innovacion": (75, 100),
            "creatividad": (70, 100)
        },
        "indicadores_secundarios": {
            "futuro": (65, 100),
            "ia": (58, 100),
            "programacion": (55, 100),
        },
        "carreras": [
            {
                "nombre": "Ingeniería en Inteligencia Artificial",
                "match_base": 94,
                "factores": {
                    "ia": 0.40,
                    "programacion": 0.25,
                    "matematicas": 0.20,
                    "innovacion": 0.15
                }
            },
            {
                "nombre": "Ingeniería Mecatrónica",
                "match_base": 90,
                "factores": {
                    "tecnologia": 0.30,
                    "ingenieria": 0.30,
                    "automatizacion": 0.25,
                    "innovacion": 0.15
                }
            },
            {
                "nombre": "Diseño de Productos Digitales",
                "match_base": 87,
                "factores": {
                    "diseno": 0.35,
                    "ux": 0.30,
                    "tecnologia": 0.20,
                    "creatividad": 0.15
                }
            }
        ],
        "descripcion": "Tu perfil combina creatividad con habilidades técnicas avanzadas. Te atrae crear soluciones innovadoras que integran múltiples disciplinas y tecnologías emergentes.",
        "fortalezas_especificas": [
            "Pensamiento interdisciplinario",
            "Adaptabilidad a nuevas tecnologías",
            "Visión de futuro y tendencias",
            "Creatividad aplicada a soluciones técnicas"
        ],
        "areas_desarrollo": [
            "Profundización en fundamentos teóricos",
            "Metodologías de investigación formal",
            "Gestión de proyectos de I+D",
            "Comercialización de innovaciones"
        ],
        "campo_laboral": [
            "Departamentos de I+D",
            "Startups tecnológicas",
            "Empresas de robótica e IA",
            "Laboratorios de innovación",
            "Emprendimiento tecnológico"
        ]
    },
    
    "ingeniero_ambiental": {
        "nombre": "Ingeniero/a Ambiental",
        "indicadores_clave": {
            "ambiental": (75, 100),
            "sostenibilidad": (75, 100),
            "ingenieria": (65, 100)
        },
        "indicadores_secundarios": {
            "ciencias": (60, 100),
            "responsabilidad": (70, 100),
            "energia": (55, 100),
        },
        "carreras": [
            {
                "nombre": "Ingeniería Ambiental",
                "match_base": 95,
                "factores": {
                    "ambiental": 0.40,
                    "sostenibilidad": 0.30,
                    "ingenieria": 0.20,
                    "ciencias": 0.10
                }
            },
            {
                "nombre": "Ingeniería en Energías Renovables",
                "match_base": 92,
                "factores": {
                    "energia": 0.40,
                    "sostenibilidad": 0.30,
                    "tecnologia": 0.20,
                    "futuro": 0.10
                }
            },
            {
                "nombre": "Ciencias Ambientales",
                "match_base": 88,
                "factores": {
                    "ambiental": 0.35,
                    "ciencias": 0.35,
                    "investigacion": 0.20,
                    "naturaleza": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil muestra una fuerte conciencia ambiental combinada con habilidades técnicas. Te motiva crear soluciones sostenibles para los desafíos ambientales actuales.",
        "fortalezas_especificas": [
            "Conciencia ambiental y sostenibilidad",
            "Pensamiento sistémico",
            "Capacidad de integrar ciencia e ingeniería",
            "Visión de largo plazo"
        ],
        "areas_desarrollo": [
            "Política pública y regulación ambiental",
            "Tecnologías emergentes en energía",
            "Análisis de ciclo de vida",
            "Comunicación de impacto ambiental"
        ],
        "campo_laboral": [
            "Consultoras ambientales",
            "Empresas de energías renovables",
            "ONGs ambientales",
            "Sector público (medio ambiente)",
            "Certificación y auditoría ambiental"
        ]
    },
    "comunicador_creativo": {
        "nombre": "Comunicador/a Creativo/a",
        "indicadores_clave": {
            "comunicacion": (70, 100),
            "creatividad": (72, 100),
            "marketing": (65, 100)
        },
        "indicadores_secundarios": {
            "diseno": (60, 100),
            "ventas": (55, 100),
            "ux": (50, 100)
        },
        "carreras": [
            {
                "nombre": "Comunicación Social",
                "match_base": 92,
                "factores": {
                    "comunicacion": 0.40,
                    "creatividad": 0.30,
                    "marketing": 0.20,
                    "ventas": 0.10
                }
            },
            {
                "nombre": "Diseño Gráfico",
                "match_base": 90,
                "factores": {
                    "diseno": 0.40,
                    "creatividad": 0.35,
                    "ux": 0.15,
                    "tecnologia": 0.10
                }
            },
            {
                "nombre": "Publicidad y Marketing",
                "match_base": 94,
                "factores": {
                    "marketing": 0.40,
                    "creatividad": 0.30,
                    "comunicacion": 0.20,
                    "negocios": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil destaca en comunicación, creatividad y conexión con audiencias. Tienes habilidad para transmitir ideas de forma impactante y generar contenido que resuena con las personas.",
        "fortalezas_especificas": [
            "Creatividad aplicada a la comunicación",
            "Capacidad de storytelling y narrativa",
            "Comprensión de audiencias y tendencias",
            "Habilidades visuales y estéticas"
        ],
        "areas_desarrollo": [
            "Análisis de datos y métricas",
            "Herramientas digitales avanzadas",
            "Estrategia de negocios",
            "Gestión de proyectos"
        ],
        "campo_laboral": [
            "Agencias de publicidad y marketing",
            "Departamentos de comunicación corporativa",
            "Producción de contenido digital",
            "Diseño de marca y branding",
            "Consultoría creativa"
        ]
    },
    
    "analista_datos": {
        "nombre": "Analista de Datos",
        "indicadores_clave": {
            "datos": (75, 100),
            "analitico": (73, 100),
            "matematicas": (68, 100)
        },
        "indicadores_secundarios": {
            "estadistica": (65, 100),
            "programacion": (55, 100),
            "logica": (60, 100)
        },
        "carreras": [
            {
                "nombre": "Ciencia de Datos",
                "match_base": 95,
                "factores": {
                    "datos": 0.40,
                    "analitico": 0.30,
                    "programacion": 0.20,
                    "matematicas": 0.10
                }
            },
            {
                "nombre": "Estadística",
                "match_base": 92,
                "factores": {
                    "estadistica": 0.40,
                    "matematicas": 0.30,
                    "analitico": 0.20,
                    "datos": 0.10
                }
            },
            {
                "nombre": "Business Intelligence",
                "match_base": 88,
                "factores": {
                    "datos": 0.35,
                    "analitico": 0.30,
                    "negocios": 0.20,
                    "tecnologia": 0.15
                }
            }
        ],
        "descripcion": "Tu perfil combina fuerte capacidad analítica con habilidades matemáticas y pasión por los datos. Destacas en encontrar patrones, hacer proyecciones y convertir datos en insights accionables.",
        "fortalezas_especificas": [
            "Análisis cuantitativo avanzado",
            "Interpretación de datos complejos",
            "Pensamiento estadístico",
            "Visualización de información"
        ],
        "areas_desarrollo": [
            "Programación avanzada (Python, R)",
            "Machine Learning aplicado",
            "Comunicación de insights a no técnicos",
            "Big Data y herramientas cloud"
        ],
        "campo_laboral": [
            "Empresas de tecnología y fintech",
            "Consultoras de análisis",
            "Departamentos de Business Intelligence",
            "Investigación de mercados",
            "Gobierno y políticas públicas"
        ]
    },
    
    "gestor_proyectos": {
        "nombre": "Gestor/a de Proyectos",
        "indicadores_clave": {
            "organizacion": (72, 100),
            "liderazgo": (70, 100),
            "gestion": (70, 100)
        },
        "indicadores_secundarios": {
            "comunicacion": (65, 100),
            "estrategia": (60, 100),
            "negocios": (55, 100)
        },
        "carreras": [
            {
                "nombre": "Administración de Empresas",
                "match_base": 90,
                "factores": {
                    "gestion": 0.35,
                    "liderazgo": 0.30,
                    "negocios": 0.20,
                    "organizacion": 0.15
                }
            },
            {
                "nombre": "Ingeniería Industrial",
                "match_base": 88,
                "factores": {
                    "organizacion": 0.35,
                    "optimizacion": 0.30,
                    "gestion": 0.20,
                    "ingenieria": 0.15
                }
            },
            {
                "nombre": "Gestión de Proyectos",
                "match_base": 93,
                "factores": {
                    "gestion": 0.40,
                    "organizacion": 0.30,
                    "liderazgo": 0.20,
                    "estrategia": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil destaca en organización, liderazgo y coordinación de recursos. Tienes la capacidad de planificar, ejecutar y entregar proyectos cumpliendo objetivos y plazos.",
        "fortalezas_especificas": [
            "Planificación estratégica",
            "Coordinación de equipos multidisciplinarios",
            "Gestión de recursos y presupuestos",
            "Resolución de conflictos"
        ],
        "areas_desarrollo": [
            "Metodologías ágiles (Scrum, Kanban)",
            "Herramientas de gestión de proyectos",
            "Habilidades técnicas específicas",
            "Negociación y manejo de stakeholders"
        ],
        "campo_laboral": [
            "Project Manager en empresas de cualquier sector",
            "Consultoría de gestión",
            "Coordinación de proyectos de desarrollo",
            "Startups y empresas tecnológicas",
            "ONGs y sector público"
        ]
    },
    "perfil_exploratorio": {
        "nombre": "Perfil en Exploración Vocacional",
        "indicadores_clave": {},
        "indicadores_secundarios": {},
        "carreras": [
            {"nombre": "Se recomienda realizar tests adicionales específicos", "afinidad": 0},
            {"nombre": "Consultar con orientador vocacional profesional", "afinidad": 0},
            {"nombre": "Explorar diferentes áreas mediante cursos introductorios", "afinidad": 0}
        ],
        "descripcion": "Tus respuestas no muestran una orientación clara hacia un perfil específico. Esto puede deberse a que aún estás explorando tus intereses o las respuestas presentan inconsistencias. Te recomendamos reflexionar más sobre las actividades que realmente disfrutas.",
        "fortalezas_especificas": [
            "Apertura a múltiples opciones profesionales",
            "Flexibilidad en intereses vocacionales",
            "Oportunidad de descubrir nuevas pasiones",
            "Capacidad de exploración sin límites preconcebidos"
        ],
        "areas_desarrollo": [
            "Definir intereses más específicos",
            "Realizar tests vocacionales especializados por área",
            "Probar actividades prácticas en diferentes campos",
            "Conversar con profesionales de distintas carreras",
            "Reflexionar sobre experiencias pasadas que te motivaron"
        ],
        "campo_laboral": []
    }
}  # ← Este } cierra PERFILES_DETALLADOS



# ================================
# FUNCIÓN PRINCIPAL DE EVALUACIÓN
# ================================

def calcular_puntajes_dimensiones(respuestas: dict) -> Dict[str, float]:
    """
    Calcula puntajes normalizados para cada dimensión vocacional
    basándose en el mapeo de preguntas
    """
    dimensiones = {}
    conteos = {}
    
    for pregunta, respuesta in respuestas.items():
        num_pregunta = int(pregunta.split("_")[1])
        puntos = PUNTUACION_VALORES.get(respuesta, 3)  # 1-5
        
        if num_pregunta in MAPEO_PREGUNTAS_GENERAL:
            pesos = MAPEO_PREGUNTAS_GENERAL[num_pregunta]
            
            for dimension, peso in pesos.items():
                if dimension not in dimensiones:
                    dimensiones[dimension] = 0
                    conteos[dimension] = 0
                
                dimensiones[dimension] += puntos * peso
                conteos[dimension] += peso
    
    # Normalizar a escala 0-100
    puntajes_normalizados = {}
    for dimension, suma in dimensiones.items():
        if conteos[dimension] > 0:
            promedio = suma / conteos[dimension]  # 1-5
            puntajes_normalizados[dimension] = round((promedio / 5) * 100, 2)
    
    return puntajes_normalizados

def detectar_contradicciones_dimensiones(puntajes: Dict[str, float]) -> int:
    """
    Detecta contradicciones graves en las dimensiones del usuario
    Retorna el número de contradicciones encontradas
    """
    contradicciones = 0
    
    # Definir pares de dimensiones que deberían ser consistentes
    pares_relacionados = [
        # (dimensión1, dimensión2, umbral_diferencia_máxima)
        ("programacion", "tecnologia", 25),  # Si programas, debes gustar de tecnología
        ("programacion", "desarrollo", 20),   # Programación y desarrollo van juntos
        ("ciencias", "investigacion", 25),    # Ciencias implica investigación
        ("biologia", "ciencias", 20),         # Biología es una ciencia
        ("quimica", "ciencias", 20),          # Química es una ciencia
        ("fisica", "ciencias", 20),           # Física es una ciencia
        ("ingenieria", "matematicas", 30),    # Ingeniería requiere matemáticas
        ("finanzas", "negocios", 25),         # Finanzas es parte de negocios
        ("marketing", "comunicacion", 25),    # Marketing requiere comunicación
        ("liderazgo", "gestion", 20),         # Liderazgo y gestión relacionados
        ("datos", "analitico", 25),           # Análisis de datos requiere ser analítico
        ("ia", "programacion", 30),           # IA requiere programación
        ("ux", "diseno", 20),                 # UX es diseño
        ("ambiental", "sostenibilidad", 15),  # Van muy de la mano
    ]
    
    for dim1, dim2, umbral in pares_relacionados:
        val1 = puntajes.get(dim1, 0)
        val2 = puntajes.get(dim2, 0)
        
        # Solo evaluar si ambas dimensiones tienen valores significativos
        if val1 > 30 or val2 > 30:
            diferencia = abs(val1 - val2)
            
            # Contradicción: diferencia excede el umbral
            if diferencia > umbral:
                # Contradicción grave: uno muy alto y otro muy bajo
                if (val1 > 70 and val2 < 40) or (val2 > 70 and val1 < 40):
                    contradicciones += 1
    
    return contradicciones

def identificar_perfil_optimo(puntajes: Dict[str, float]) -> Tuple[str, float]:
    """
    Identifica el perfil con VALIDACIÓN ESTRICTA + DETECTOR DE CONTRADICCIONES
    """
    # 🔍 PASO 0: Detectar contradicciones graves
    contradicciones = detectar_contradicciones_dimensiones(puntajes)
    if contradicciones > 3:
        return "perfil_exploratorio", 0
    
    scores_perfiles = {}
    
    for perfil_id, perfil in PERFILES_DETALLADOS.items():
        # 🎯 PASO 1: Verificar indicadores clave (REQUISITOS DUROS)
        
        # ⚠️ FIX: Verificar que tenga indicadores clave
        if not perfil.get("indicadores_clave") or len(perfil["indicadores_clave"]) == 0:
            # Si no tiene indicadores clave, saltar este perfil
            scores_perfiles[perfil_id] = 0
            continue
        
        cumple_requisitos_minimos = True
        score_indicadores_clave = 0
        indicadores_cumplidos = 0
        
        for indicador, (min_val, max_val) in perfil["indicadores_clave"].items():
            puntaje_usuario = puntajes.get(indicador, 0)
            
            # Umbral de descalificación: 70% del mínimo
            if puntaje_usuario < min_val * 0.7:
                cumple_requisitos_minimos = False
                break
            
            # Calcular score según rango
            if min_val <= puntaje_usuario <= max_val:
                # Rango óptimo
                score_indicadores_clave += 100
                indicadores_cumplidos += 1
            elif puntaje_usuario < min_val:
                # Por debajo pero no descalificado
                diferencia = min_val - puntaje_usuario
                score_indicadores_clave += max(0, 100 - (diferencia * 2.5))
            else:
                # Por encima del máximo (aceptable)
                score_indicadores_clave += 88
                indicadores_cumplidos += 1
        
        if not cumple_requisitos_minimos:
            scores_perfiles[perfil_id] = 0
            continue
        
        # 🔥 FIX: Verificar que cumple al menos 70% de indicadores clave
        porcentaje_cumplimiento = (indicadores_cumplidos / len(perfil["indicadores_clave"])) * 100
        if porcentaje_cumplimiento < 70:
            scores_perfiles[perfil_id] = 0
            continue
        
        # 🎯 PASO 2: Evaluar indicadores secundarios (bonificación)
        score_secundarios = 0
        for indicador, (min_val, max_val) in perfil.get("indicadores_secundarios", {}).items():
            puntaje_usuario = puntajes.get(indicador, 0)
            
            if min_val <= puntaje_usuario <= max_val:
                score_secundarios += 55
            elif puntaje_usuario >= min_val * 0.8:
                score_secundarios += 35
        
        # 🎯 PASO 3: Calcular score normalizado
        total_posible = (
            len(perfil["indicadores_clave"]) * 100 +
            len(perfil.get("indicadores_secundarios", {})) * 55
        )
        
        if total_posible > 0:
            score_final = ((score_indicadores_clave + score_secundarios) / total_posible) * 100
            
            # 🔥 Penalización por falta de dimensiones fuertes
            dimensiones_fuertes = sum(1 for v in puntajes.values() if v >= 68)
            if dimensiones_fuertes < 3:
                score_final *= 0.82
            elif dimensiones_fuertes >= 6:
                score_final *= 1.05
            
            # 🔥 Penalización por contradicciones
            if contradicciones > 0:
                score_final *= (1 - (contradicciones * 0.08))
            
            scores_perfiles[perfil_id] = round(min(score_final, 100), 2)
        else:
            scores_perfiles[perfil_id] = 0
    
    # 🎯 PASO 4: Validación final - Umbral mínimo 50%
    if not scores_perfiles or max(scores_perfiles.values()) < 50:
        return "perfil_exploratorio", max(scores_perfiles.values(), default=0)
    
    mejor_perfil = max(scores_perfiles, key=scores_perfiles.get)
    return mejor_perfil, scores_perfiles[mejor_perfil]

def calcular_match_carreras(perfil_data: dict, puntajes: Dict[str, float]) -> List[dict]:
    """
    Calcula match con VALIDACIÓN REALISTA de coherencia
    """
    carreras_con_match = []
    
    for carrera in perfil_data["carreras"]:
        match_base = carrera["match_base"]
        
        # Verificar coherencia con factores requeridos
        factores_cumplidos = 0
        factores_fuertes = 0  # Factores > 70%
        suma_ajustes = 0
        
        for factor, peso in carrera["factores"].items():
            puntaje_factor = puntajes.get(factor, 0)
            
            # Contar factores con puntaje decente (≥45%)
            if puntaje_factor >= 45:
                factores_cumplidos += 1
                
                # Contar factores fuertes
                if puntaje_factor >= 70:
                    factores_fuertes += 1
                
                # Calcular ajuste (más conservador)
                ajuste = ((puntaje_factor - 50) / 50) * peso * 8  # Máximo ±8 por factor
                suma_ajustes += ajuste
            else:
                # Penalización por factor débil
                suma_ajustes -= peso * 5
        
        # Calcular porcentajes
        porcentaje_cumplimiento = (factores_cumplidos / len(carrera["factores"])) * 100
        porcentaje_fuertes = (factores_fuertes / len(carrera["factores"])) * 100
        
        # Aplicar lógica de penalizaciones/bonificaciones
        if porcentaje_cumplimiento < 50:
            # Menos del 50% de factores cumplidos = penalización fuerte
            match_calculado = match_base * 0.6
        elif porcentaje_cumplimiento < 75:
            # Entre 50-75% = penalización moderada
            match_calculado = match_base * 0.85 + suma_ajustes
        else:
            # 75%+ cumplimiento = aplicar ajustes normales
            match_calculado = match_base + suma_ajustes
            
            # Bonificación si tiene muchos factores fuertes
            if porcentaje_fuertes >= 50:
                match_calculado *= 1.05  # +5% bonus
        
        # Limitar a rango realista: 35-97%
        match_calculado = max(35, min(97, match_calculado))
        
        carreras_con_match.append({
            "nombre": carrera["nombre"],
            "afinidad": round(match_calculado, 2)
        })
    
    # Ordenar por afinidad descendente
    return sorted(carreras_con_match, key=lambda x: x["afinidad"], reverse=True)

def calcular_resultados_test(tipo_test: str, respuestas: dict) -> dict:
    """
    Función principal mejorada de cálculo de resultados
    """
    # Calcular puntuación total tradicional
    puntuacion_total = sum(PUNTUACION_VALORES.get(v, 0) for v in respuestas.values())
    total_preguntas = len(respuestas)
    puntuacion_maxima = total_preguntas * 5
    porcentaje_global = round((puntuacion_total / puntuacion_maxima) * 100, 2)
    
    # Calcular puntajes por dimensión
    puntajes_dimensiones = calcular_puntajes_dimensiones(respuestas)
    
    # Identificar perfil óptimo
    perfil_id, score_ajuste = identificar_perfil_optimo(puntajes_dimensiones)
    
    # 🔥 NUEVO: Manejo de perfil exploratorio
    # 🔥 NUEVO: Manejo de perfil exploratorio
    if perfil_id == "perfil_exploratorio":
        return {
            "puntuacion_total": puntuacion_total,
            "puntuacion_maxima": puntuacion_maxima,
            "porcentaje_afinidad": score_ajuste,
            "porcentaje_global": porcentaje_global,
            "nivel": "Exploratoria",
            "mensaje": "Tus respuestas indican que aún estás explorando tus intereses vocacionales. "
                    "Te recomendamos realizar tests adicionales específicos o reflexionar más sobre "
                    "las actividades que realmente te apasionan. No hay un perfil dominante claro en este momento.",
            "area_principal": "En Exploración",
            "carreras_recomendadas": [
                {"nombre": "Realiza tests específicos por área", "afinidad": 0},
                {"nombre": "Consulta con un orientador vocacional", "afinidad": 0}
            ],
            "fortalezas": [
                "Apertura a explorar diferentes opciones",
                "Flexibilidad en intereses",
                "Oportunidad de descubrir nuevas pasiones"
            ],
            "areas_desarrollo": [
                "Definir intereses más específicos",
                "Probar actividades prácticas en diferentes áreas",
                "Realizar tests vocacionales especializados",
                "Conversar con profesionales de distintas áreas"
            ],
            "campo_laboral": [],
            "puntajes_dimensiones": puntajes_dimensiones,
            "perfil_identificado": "exploratorio",
            "score_ajuste": score_ajuste
        }
        
    # Perfil definido - continuar con lógica normal
    perfil_data = PERFILES_DETALLADOS[perfil_id]
    carreras_recomendadas = calcular_match_carreras(perfil_data, puntajes_dimensiones)
    
    # Determinar nivel de claridad vocacional
    if score_ajuste >= 75:
        nivel = "Excelente"
        claridad = "muy clara"
    elif score_ajuste >= 60:
        nivel = "Buena"
        claridad = "clara"
    elif score_ajuste >= 45:
        nivel = "Moderada"
        claridad = "moderada"
    else:
        nivel = "Exploratoria"
        claridad = "en exploración"
    
    # Mensaje personalizado
    mensaje = f"{perfil_data['descripcion']}\n\nTu orientación vocacional es {claridad} hacia este perfil (ajuste: {score_ajuste}%). "
    
    if score_ajuste >= 70:
        mensaje += "Las carreras recomendadas tienen un alto nivel de compatibilidad con tus intereses y habilidades."
    elif score_ajuste >= 50:
        mensaje += "Te recomendamos explorar más sobre las carreras sugeridas para validar tu interés."
    else:
        mensaje += "Considera tomar tests adicionales o explorar otras áreas para clarificar tu vocación."
    
    return {
        "puntuacion_total": puntuacion_total,
        "puntuacion_maxima": puntuacion_maxima,
        "porcentaje_afinidad": score_ajuste,
        "porcentaje_global": porcentaje_global,
        "nivel": nivel,
        "mensaje": mensaje,
        "area_principal": perfil_data["nombre"],
        "carreras_recomendadas": carreras_recomendadas[:5],
        "fortalezas": perfil_data["fortalezas_especificas"],
        "areas_desarrollo": perfil_data["areas_desarrollo"],
        "campo_laboral": perfil_data.get("campo_laboral", []),
        "puntajes_dimensiones": puntajes_dimensiones,
        "perfil_identificado": perfil_id,
        "score_ajuste": score_ajuste
    }

# ================================
# RUTAS DE PÁGINAS PRINCIPALES
# ================================

@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/blog", response_class=HTMLResponse, name="blog")
async def blog(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("blog.html", {"request": request, "user": user})

@app.get("/carrerasdem", response_class=HTMLResponse, name="carrerasdem")
async def carrerasdem(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("carrerasdem.html", {"request": request, "user": user})

@app.get("/comoelegir", response_class=HTMLResponse, name="comoelegir")
async def como_elegir(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("comoelegir.html", {"request": request, "user": user})

@app.get("/errorescom", response_class=HTMLResponse, name="errorescom")
async def errores_comunes(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("errores.html", {"request": request, "user": user})

@app.get("/fechasimp", response_class=HTMLResponse, name="fechasimp")
async def fechas_importantes(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("fechasimp.html", {"request": request, "user": user})

@app.get("/guiav", response_class=HTMLResponse, name="guiav")
async def guia_vocacional(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("guiav.html", {"request": request, "user": user})

@app.get("/mitosyr", response_class=HTMLResponse, name="mitosyr")
async def mitos_y_realidades(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("mitosyr.html", {"request": request, "user": user})

@app.get("/programas", response_class=HTMLResponse, name="programas-universidades")
async def programas(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("programas-universidades.html", {"request": request, "user": user})

@app.get("/recuryevent", response_class=HTMLResponse, name="recuryevent")
async def recursos_eventos(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("recuryevent.html", {"request": request, "user": user})

@app.get("/articulos", response_class=HTMLResponse, name="articulos")
async def articulos(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("articulos.html", {"request": request, "user": user})

@app.get("/webinars", response_class=HTMLResponse, name="webinars")
async def webinars(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("webinars.html", {"request": request, "user": user})

@app.get("/becas", response_class=HTMLResponse, name="becas")
async def becas(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("becas.html", {"request": request, "user": user})

@app.get("/calculadora", response_class=HTMLResponse, name="calculadora")
async def calculadora(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("calculadora.html", {"request": request, "user": user})

# ================================
# RUTAS DE TESTS VOCACIONALES
# ================================

@app.get("/test-vocacional", response_class=HTMLResponse, name="test-vocacional")
async def test_vocacional(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("test-vocacional.html", {"request": request, "user": user})

@app.get("/test/{tipo_test}", response_class=HTMLResponse)
async def mostrar_test(request: Request, tipo_test: str, user: dict = Depends(get_current_user)):
    """Muestra el formulario del test"""
    if tipo_test not in TESTS_CONFIG:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "mensaje": "Test no encontrado", "user": user},
            status_code=404
        )
    
    test_data = TESTS_CONFIG[tipo_test]
    return templates.TemplateResponse(
        "test.html",
        {
            "request": request,
            "user": user,
            "tipo": tipo_test,
            "titulo": test_data["titulo"],
            "descripcion": test_data["descripcion"],
            "instrucciones": test_data["instrucciones"],
            "preguntas": test_data["preguntas"],
            "total_preguntas": len(test_data["preguntas"])
        }
    )

@app.post("/test/{tipo_test}/procesar")
async def procesar_test(
    tipo_test: str,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Procesa las respuestas del test y las guarda en la base de datos"""
    try:
        # 1. Obtener respuestas del formulario
        form_data = await request.form()
        respuestas = {k: v for k, v in form_data.items() if k.startswith("pregunta_")}
        
        # 2. Validar que todas las preguntas fueron respondidas
        total_preguntas = len(TESTS_CONFIG[tipo_test]["preguntas"])
        if len(respuestas) != total_preguntas:
            return templates.TemplateResponse(
                "test.html",
                {
                    "request": request,
                    "user": user,
                    "tipo": tipo_test,
                    "titulo": TESTS_CONFIG[tipo_test]["titulo"],
                    "descripcion": TESTS_CONFIG[tipo_test]["descripcion"],
                    "instrucciones": TESTS_CONFIG[tipo_test]["instrucciones"],
                    "preguntas": TESTS_CONFIG[tipo_test]["preguntas"],
                    "total_preguntas": total_preguntas,
                    "error": "⚠️ Por favor responde todas las preguntas antes de continuar"
                }
            )
        
        # 3. Calcular resultados
        resultados = calcular_resultados_test(tipo_test, respuestas)
        
        # 4. Guardar en base de datos
        test_id = None
        test_guardado = False
        
        if user:
            try:
                print(f"💾 Guardando test para usuario ID: {user['id']}")
                
                # 4.1 Insertar test principal
                query_test = text("""
                    INSERT INTO tests_realizados 
                    (usuario_id, tipo_test, puntuacion_total, completado, fecha_realizacion)
                    VALUES (:user_id, :tipo, :puntuacion, true, CURRENT_TIMESTAMP)
                    RETURNING id
                """)
                
                result = db.execute(query_test, {
                    "user_id": user["id"],
                    "tipo": tipo_test,
                    "puntuacion": resultados["puntuacion_total"]
                })
                
                test_id = result.fetchone()[0]
                print(f"✅ Test creado con ID: {test_id}")
                
                # 4.2 Guardar respuestas individuales
                for pregunta, respuesta in respuestas.items():
                    pregunta_num = int(pregunta.split("_")[1])
                    
                    query_respuesta = text("""
                        INSERT INTO respuestas_test 
                        (test_id, pregunta_id, respuesta, puntos)
                        VALUES (:test_id, :pregunta_id, :respuesta, :puntos)
                    """)
                    
                    db.execute(query_respuesta, {
                        "test_id": test_id,
                        "pregunta_id": pregunta_num,
                        "respuesta": respuesta,
                        "puntos": PUNTUACION_VALORES.get(respuesta, 3)
                    })
                
                print(f"✅ {len(respuestas)} respuestas guardadas")
                
                # 4.3 Preparar datos adicionales en formato JSON
                datos_adicionales = {
                    "perfil_identificado": resultados.get("perfil_identificado", ""),
                    "score_ajuste": float(resultados.get("score_ajuste", 0)),
                    "porcentaje_global": float(resultados.get("porcentaje_global", 0)),
                    "puntajes_dimensiones": resultados.get("puntajes_dimensiones", {})
                }
                
                # 4.4 Guardar resultados detallados
                query_resultado = text("""
                    INSERT INTO resultados_test 
                    (test_id, area_principal, porcentaje_afinidad, 
                     carreras_recomendadas, fortalezas, areas_desarrollo, 
                     descripcion_perfil, datos_adicionales, campo_laboral)
                    VALUES (:test_id, :area, :porcentaje, 
                            CAST(:carreras AS jsonb), 
                            :fortalezas, :desarrollo, :descripcion, 
                            CAST(:datos_adicionales AS jsonb), 
                            :campo_laboral)
                """)
                
                db.execute(query_resultado, {
                    "test_id": test_id,
                    "area": resultados["area_principal"],
                    "porcentaje": float(resultados["score_ajuste"]),
                    "carreras": json.dumps(resultados["carreras_recomendadas"]),
                    "fortalezas": resultados["fortalezas"],
                    "desarrollo": resultados["areas_desarrollo"],
                    "descripcion": resultados["mensaje"],
                    "datos_adicionales": json.dumps(datos_adicionales),
                    "campo_laboral": resultados.get("campo_laboral", [])
                })
                
                print(f"✅ Resultados guardados")
                
                # ⚠️ CRÍTICO: Hacer commit
                db.commit()
                test_guardado = True
                print(f"🎉 Test {test_id} guardado completamente")
                
            except Exception as e:
                db.rollback()
                print(f"❌ ERROR al guardar test: {str(e)}")
                import traceback
                traceback.print_exc()
                test_guardado = False
        else:
            print("ℹ️ Usuario no autenticado - test no guardado")
        
        # 5. Mostrar resultados
        return templates.TemplateResponse(
            "resultado_test.html",
            {
                "request": request,
                "user": user,
                "tipo": tipo_test,
                "resultados": resultados,
                "test_config": TESTS_CONFIG[tipo_test],
                "test_guardado": test_guardado,
                "test_id": test_id
            }
        )
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "user": user,
                "mensaje": f"Error al procesar el test: {str(e)}"
            },
            status_code=500
        )


# ================================
# RUTA PARA VER DETALLE MEJORADO
# ================================

@app.get("/test/{test_id}/detalle", response_class=HTMLResponse)
async def detalle_test(
    test_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Muestra el detalle de un test con análisis mejorado"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Obtener datos del test
        query = text("""
            SELECT 
                t.tipo_test,
                t.fecha_realizacion,
                t.puntuacion_total,
                r.area_principal,
                r.porcentaje_afinidad,
                r.carreras_recomendadas,
                r.fortalezas,
                r.areas_desarrollo,
                r.descripcion_perfil,
                r.datos_adicionales,
                r.campo_laboral
            FROM tests_realizados t
            LEFT JOIN resultados_test r ON t.id = r.test_id
            WHERE t.id = :test_id AND t.usuario_id = :user_id
        """)
        
        result = db.execute(query, {
            "test_id": test_id,
            "user_id": user["id"]
        }).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Test no encontrado")
        
        # Parsear datos JSON
        carreras = []
        if result[5]:
            try:
                carreras = json.loads(result[5]) if isinstance(result[5], str) else result[5]
            except:
                carreras = []
        
        datos_adicionales = {}
        if result[9]:
            try:
                datos_adicionales = json.loads(result[9]) if isinstance(result[9], str) else result[9]
            except:
                datos_adicionales = {}
        
        campo_laboral = result[10] or []
        
        # Construir objeto de resultados completo
        resultados = {
            "porcentaje_afinidad": result[4],
            "score_ajuste": datos_adicionales.get("score_ajuste", result[4]),
            "porcentaje_global": datos_adicionales.get("porcentaje_global", result[4]),
            "nivel": "Excelente" if result[4] >= 75 else "Buena" if result[4] >= 60 else "Moderada" if result[4] >= 45 else "Exploratoria",
            "mensaje": result[8],
            "area_principal": result[3],
            "carreras_recomendadas": carreras,
            "fortalezas": result[6] or [],
            "areas_desarrollo": result[7] or [],
            "campo_laboral": campo_laboral,
            "datos_adicionales": datos_adicionales,
            "puntajes_dimensiones": datos_adicionales.get("puntajes_dimensiones", {}),
            "top_dimensiones": datos_adicionales.get("top_dimensiones", [])
        }
        
        return templates.TemplateResponse(
            "resultado_test_detallado.html",  # Nueva plantilla mejorada
            {
                "request": request,
                "user": user,
                "tipo": result[0],
                "fecha_realizacion": result[1],
                "puntuacion_total": result[2],
                "resultados": resultados,
                "test_config": TESTS_CONFIG.get(result[0], TESTS_CONFIG["general"]),
                "es_historico": True,
                "test_id": test_id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener detalle: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al cargar el test")


# ================================
# NUEVA RUTA: ANÁLISIS COMPARATIVO
# ================================

@app.get("/analisis-vocacional", response_class=HTMLResponse, name="analisis_vocacional")
async def analisis_vocacional(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Muestra análisis comparativo y evolución del usuario"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Obtener todos los tests del usuario
        query = text("""
            SELECT 
                t.id,
                t.tipo_test,
                t.fecha_realizacion,
                t.puntuacion_total,
                r.porcentaje_afinidad,
                r.area_principal,
                r.datos_adicionales
            FROM tests_realizados t
            LEFT JOIN resultados_test r ON t.id = r.test_id
            WHERE t.usuario_id = :user_id AND t.completado = true
            ORDER BY t.fecha_realizacion DESC
        """)
        
        tests = db.execute(query, {"user_id": user["id"]}).fetchall()
        
        # Procesar datos para análisis
        tests_procesados = []
        analisis_dimensional = {}
        
        for test in tests:
            datos_adicionales = {}
            if test[6]:
                try:
                    datos_adicionales = json.loads(test[6]) if isinstance(test[6], str) else test[6]
                except:
                    pass
            
            test_data = {
                "id": test[0],
                "tipo": test[1],
                "fecha": test[2],
                "puntuacion": test[3],
                "porcentaje": test[4],
                "area": test[5],
                "perfil": datos_adicionales.get("perfil_identificado", ""),
                "score_ajuste": datos_adicionales.get("score_ajuste", 0),
                "puntajes_dimensiones": datos_adicionales.get("puntajes_dimensiones", {})
            }
            tests_procesados.append(test_data)
            
            # Acumular puntajes dimensionales para análisis agregado
            for dimension, puntaje in test_data["puntajes_dimensiones"].items():
                if dimension not in analisis_dimensional:
                    analisis_dimensional[dimension] = []
                analisis_dimensional[dimension].append({
                    "fecha": test[2],
                    "puntaje": puntaje,
                    "tipo_test": test[1]
                })
        
        # Calcular promedios y tendencias
        dimensiones_promedio = {}
        for dimension, historial in analisis_dimensional.items():
            puntajes = [h["puntaje"] for h in historial]
            dimensiones_promedio[dimension] = {
                "promedio": round(sum(puntajes) / len(puntajes), 2),
                "minimo": min(puntajes),
                "maximo": max(puntajes),
                "tendencia": "ascendente" if len(puntajes) > 1 and puntajes[-1] > puntajes[0] else "estable"
            }
        
        # Identificar top 5 dimensiones más fuertes
        top_dimensiones = sorted(
            dimensiones_promedio.items(),
            key=lambda x: x[1]["promedio"],
            reverse=True
        )[:5]
        
        # Calcular evolución si hay tests del mismo tipo
        evolucion = calcular_evolucion_por_tipo(tests_procesados)
        
        return templates.TemplateResponse(
            "analisis_vocacional.html",
            {
                "request": request,
                "user": user,
                "tests": tests_procesados,
                "total_tests": len(tests_procesados),
                "dimensiones_promedio": dimensiones_promedio,
                "top_dimensiones": top_dimensiones,
                "evolucion": evolucion,
                "tiene_datos": len(tests_procesados) > 0
            }
        )
        
    except Exception as e:
        print(f"❌ Error en análisis vocacional: {e}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "user": user,
                "mensaje": "Error al generar el análisis vocacional"
            }
        )


def calcular_evolucion_por_tipo(tests: list) -> dict:
    """Calcula la evolución del usuario por tipo de test"""
    evolucion = {}
    
    # Agrupar por tipo
    por_tipo = {}
    for test in tests:
        tipo = test["tipo"]
        if tipo not in por_tipo:
            por_tipo[tipo] = []
        por_tipo[tipo].append(test)
    
    # Analizar evolución para cada tipo
    for tipo, tests_tipo in por_tipo.items():
        if len(tests_tipo) < 2:
            continue
        
        # Ordenar por fecha
        tests_ordenados = sorted(tests_tipo, key=lambda x: x["fecha"])
        
        primer = tests_ordenados[0]
        ultimo = tests_ordenados[-1]
        
        diferencia = ultimo["score_ajuste"] - primer["score_ajuste"]
        
        evolucion[tipo] = {
            "primer_score": primer["score_ajuste"],
            "ultimo_score": ultimo["score_ajuste"],
            "diferencia": round(diferencia, 2),
            "mejora": diferencia > 0,
            "cantidad": len(tests_tipo),
            "primer_fecha": primer["fecha"],
            "ultima_fecha": ultimo["fecha"],
            "primer_perfil": primer.get("perfil", ""),
            "ultimo_perfil": ultimo.get("perfil", ""),
            "cambio_perfil": primer.get("perfil") != ultimo.get("perfil")
        }
    
    return evolucion


# ================================
# NUEVA RUTA: EXPORTAR RESULTADOS
# ================================

@app.get("/test/{test_id}/exportar-pdf")
async def exportar_pdf(
    test_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Genera un PDF con los resultados del test (futuro)"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Por ahora, redirect a detalle
    # En el futuro, usar reportlab o weasyprint para generar PDF
    return RedirectResponse(url=f"/test/{test_id}/detalle", status_code=303)


# ================================
# API: OBTENER DIMENSIONES DEL USUARIO
# ================================

@app.get("/api/usuario/dimensiones")
async def get_dimensiones_usuario(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """API para obtener las dimensiones vocacionales del usuario"""
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        query = text("""
            SELECT 
                r.datos_adicionales->'puntajes_dimensiones' as dimensiones,
                t.fecha_realizacion
            FROM tests_realizados t
            LEFT JOIN resultados_test r ON t.id = r.test_id
            WHERE t.usuario_id = :user_id 
            AND t.tipo_test = 'general'
            AND r.datos_adicionales IS NOT NULL
            ORDER BY t.fecha_realizacion DESC
            LIMIT 1
        """)
        
        result = db.execute(query, {"user_id": user["id"]}).fetchone()
        
        if not result or not result[0]:
            return {
                "success": False,
                "message": "No se encontraron tests realizados"
            }
        
        dimensiones = result[0] if isinstance(result[0], dict) else json.loads(result[0])
        
        return {
            "success": True,
            "dimensiones": dimensiones,
            "fecha_ultimo_test": result[1].isoformat() if result[1] else None
        }
        
    except Exception as e:
        print(f"❌ Error al obtener dimensiones: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener dimensiones")

@app.get("/mis-tests", response_class=HTMLResponse, name="resultados")
async def mis_tests(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Muestra el historial de tests del usuario"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        query = text("""
            SELECT 
                t.id,
                t.tipo_test,
                t.fecha_realizacion,
                t.puntuacion_total,
                r.porcentaje_afinidad,
                r.area_principal
            FROM tests_realizados t
            LEFT JOIN resultados_test r ON t.id = r.test_id
            WHERE t.usuario_id = :user_id
            ORDER BY t.fecha_realizacion DESC
        """)
        
        tests = db.execute(query, {"user_id": user["id"]}).fetchall()
        
        tests_data = []
        for test in tests:
            tests_data.append({
                "id": test[0],
                "tipo": test[1],
                "fecha": test[2],
                "puntuacion": test[3],
                "afinidad": test[4],
                "area": test[5]
            })
        
        return templates.TemplateResponse(
            "mis_test.html",
            {
                "request": request,
                "user": user,
                "tests": tests_data
            }
        )
        
    except Exception as e:
        print(f"❌ Error al obtener tests: {e}")
        return templates.TemplateResponse(
            "mis_test.html",
            {
                "request": request,
                "user": user,
                "tests": [],
                "error": "Error al cargar el historial"
            }
        )

@app.get("/test/{test_id}/detalle", response_class=HTMLResponse)
async def detalle_test(
    test_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Muestra el detalle de un test específico"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Verificar que el test pertenece al usuario
        query = text("""
            SELECT 
                t.tipo_test,
                t.fecha_realizacion,
                t.puntuacion_total,
                r.area_principal,
                r.porcentaje_afinidad,
                r.carreras_recomendadas,
                r.fortalezas,
                r.areas_desarrollo,
                r.descripcion_perfil
            FROM tests_realizados t
            LEFT JOIN resultados_test r ON t.id = r.test_id
            WHERE t.id = :test_id AND t.usuario_id = :user_id
        """)
        
        result = db.execute(query, {
            "test_id": test_id,
            "user_id": user["id"]
        }).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Test no encontrado")
        
        # Parsear carreras si existen
        carreras = []
        if result[5]:
            try:
                carreras = json.loads(result[5]) if isinstance(result[5], str) else result[5]
            except:
                carreras = []
        
        test_data = {
            "tipo": result[0],
            "fecha": result[1],
            "puntuacion": result[2],
            "area": result[3],
            "afinidad": result[4],
            "carreras": carreras,
            "fortalezas": result[6] or [],
            "desarrollo": result[7] or [],
            "descripcion": result[8]
        }
        
        return templates.TemplateResponse(
            "resultado_test.html",
            {
                "request": request,
                "user": user,
                "tipo": test_data["tipo"],
                "resultados": {
                    "porcentaje_afinidad": test_data["afinidad"],
                    "nivel": "Excelente" if test_data["afinidad"] >= 80 else "Buena" if test_data["afinidad"] >= 65 else "Moderada",
                    "mensaje": test_data["descripcion"],
                    "area_principal": test_data["area"],
                    "carreras_recomendadas": test_data["carreras"],
                    "fortalezas": test_data["fortalezas"],
                    "areas_desarrollo": test_data["desarrollo"]
                },
                "test_config": TESTS_CONFIG.get(test_data["tipo"], TESTS_CONFIG["general"])
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener detalle: {e}")
        raise HTTPException(status_code=500, detail="Error al cargar el test")

# ================================
# RUTAS DE AUTENTICACIÓN
# ================================

@app.get("/login", response_class=HTMLResponse, name="login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(
    request: Request,
    Gmail: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        query = text("SELECT id, nombre, gmail, rol FROM usuarios WHERE gmail = :gmail AND contraseña = :pwd")
        result = db.execute(query, {"gmail": Gmail, "pwd": contraseña}).fetchone()

        if result:
            # LIMPIEZA COMPLETA DE SESIÓN
            request.session.clear()
            
            # SETEAR VALORES UNO POR UNO
            request.session["user_id"] = result[0]
            request.session["user_nombre"] = result[1]
            request.session["user_gmail"] = result[2]
            request.session["user_rol"] = result[3]
            request.session["logged_in"] = True
            
            # FORZAR MODIFICACIÓN (crítico para Vercel)
            request.session.modified = True
            
            # Debug
            if IS_PRODUCTION:
                print(f"Login PRODUCCIÓN - User: {result[1]}")
                print(f"Session: {dict(request.session)}")
            else:
                print(f"Login DESARROLLO - User ID: {result[0]}, Nombre: {result[1]}")
            
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Correo o contraseña incorrectos"}
            )
    except Exception as e:
        print(f"Error en login: {e}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Error al iniciar sesión"}
        )
        
@app.get("/api/check-session")
async def check_session(request: Request):
    """Verifica si hay sesión activa"""
    user = get_current_user(request)
    return {
        "logged_in": user is not None,
        "user": user
    }

@app.get("/register", response_class=HTMLResponse, name="register")
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_post(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    rol: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        check_query = text("SELECT * FROM usuarios WHERE gmail = :email")
        existing_user = db.execute(check_query, {"email": email}).fetchone()
        
        if existing_user:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Este correo ya está registrado"}
            )
        
        insert_query = text("""
            INSERT INTO usuarios (nombre, gmail, rol, contraseña) 
            VALUES (:nombre, :email, :rol, :contraseña)
        """)
        
        db.execute(insert_query, {
            "nombre": nombre,
            "email": email,
            "rol": rol,
            "contraseña": contraseña
        })
        db.commit()
        
        return RedirectResponse(url="/login", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al registrar usuario: {e}")
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Error al crear la cuenta. Intenta de nuevo."}
        )

@app.get("/logout", name="logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# ================================
# RUTAS DE PERFIL DE USUARIO
# ================================

@app.get("/perfil", response_class=HTMLResponse, name="perfil")
async def perfil(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("perfil.html", {"request": request, "user": user})

@app.get("/actualizar-info", response_class=HTMLResponse, name="actualizar_info")
async def actualizar_info_get(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("actualizar-info.html", {"request": request, "user": user})

@app.post("/actualizar-info")
async def actualizar_info_post(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    rol: str = Form(...),
    contraseña_actual: str = Form(None),
    contraseña_nueva: str = Form(None),
    contraseña_confirmar: str = Form(None),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        check_email_query = text("SELECT id FROM usuarios WHERE gmail = :email AND id != :user_id")
        existing_user = db.execute(check_email_query, {"email": email, "user_id": user["id"]}).fetchone()
        
        if existing_user:
            return templates.TemplateResponse(
                "actualizar-info.html",
                {"request": request, "user": user, "error": "Este correo ya está en uso por otra cuenta"}
            )
        
        if contraseña_actual or contraseña_nueva or contraseña_confirmar:
            if not all([contraseña_actual, contraseña_nueva, contraseña_confirmar]):
                return templates.TemplateResponse(
                    "actualizar-info.html",
                    {"request": request, "user": user, "error": "Debes completar todos los campos de contraseña"}
                )
            
            verify_query = text("SELECT id FROM usuarios WHERE id = :user_id AND contraseña = :pwd")
            verify_result = db.execute(verify_query, {"user_id": user["id"], "pwd": contraseña_actual}).fetchone()
            
            if not verify_result:
                return templates.TemplateResponse(
                    "actualizar-info.html",
                    {"request": request, "user": user, "error": "La contraseña actual es incorrecta"}
                )
            
            if contraseña_nueva != contraseña_confirmar:
                return templates.TemplateResponse(
                    "actualizar-info.html",
                    {"request": request, "user": user, "error": "Las contraseñas nuevas no coinciden"}
                )
            
            if len(contraseña_nueva) < 6:
                return templates.TemplateResponse(
                    "actualizar-info.html",
                    {"request": request, "user": user, "error": "La nueva contraseña debe tener al menos 6 caracteres"}
                )
            
            update_query = text("""
                UPDATE usuarios 
                SET nombre = :nombre, gmail = :email, rol = :rol, contraseña = :nueva_pwd
                WHERE id = :user_id
            """)
            db.execute(update_query, {
                "nombre": nombre,
                "email": email,
                "rol": rol,
                "nueva_pwd": contraseña_nueva,
                "user_id": user["id"]
            })
        else:
            update_query = text("""
                UPDATE usuarios 
                SET nombre = :nombre, gmail = :email, rol = :rol
                WHERE id = :user_id
            """)
            db.execute(update_query, {
                "nombre": nombre,
                "email": email,
                "rol": rol,
                "user_id": user["id"]
            })
        
        db.commit()
        
        # ACTUALIZAR SESIÓN CORRECTAMENTE
        request.session["user_nombre"] = nombre
        request.session["user_gmail"] = email
        request.session["user_rol"] = rol
        request.session.modified = True 
        
        user["nombre"] = nombre
        user["gmail"] = email
        user["rol"] = rol
        
        return templates.TemplateResponse(
            "actualizar-info.html",
            {"request": request, "user": user, "success": "Información actualizada correctamente"}
        )
        
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return templates.TemplateResponse(
            "actualizar-info.html",
            {"request": request, "user": user, "error": "Error al actualizar la información"}
        )

@app.post("/eliminar-cuenta")
async def eliminar_cuenta(
    request: Request,
    contraseña: str = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        verify_query = text("SELECT id FROM usuarios WHERE id = :user_id AND contraseña = :pwd")
        verify_result = db.execute(verify_query, {"user_id": user["id"], "pwd": contraseña}).fetchone()
        
        if not verify_result:
            return templates.TemplateResponse(
                "perfil.html",
                {"request": request, "user": user, "error": "Contraseña incorrecta"}
            )
        
        delete_query = text("DELETE FROM usuarios WHERE id = :user_id")
        db.execute(delete_query, {"user_id": user["id"]})
        db.commit()
        
        request.session.clear()
        
        return RedirectResponse(url="/", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al eliminar cuenta: {e}")
        return templates.TemplateResponse(
            "perfil.html",
            {"request": request, "user": user, "error": "Error al eliminar la cuenta. Intenta de nuevo."}
        )

# ================================
# API DE FILTROS Y BÚSQUEDA
# ================================

@app.get("/api/filtrar-carreras")
async def filtrar_carreras(
    db: Session = Depends(get_db),
    area: Optional[str] = Query(None),
    modalidad: Optional[str] = Query(None),
    duracion: Optional[str] = Query(None),
    especializacion: Optional[str] = Query(None)
):
    try:
        base_query = "SELECT nombre FROM profesiones WHERE 1=1"
        parametros = {}
        filtros = []

        if area:
            filtros.append("area = :area_val")
            parametros["area_val"] = area.strip()

        if modalidad:
            filtros.append("modalidad = :modalidad_val")
            parametros["modalidad_val"] = modalidad.strip()

        if duracion:
            filtros.append("duracion LIKE :duracion_val")
            parametros["duracion_val"] = f"%{duracion.strip()}%"

        if especializacion:
            filtros.append("especializacion = :esp_val")
            parametros["esp_val"] = especializacion.strip()

        if filtros:
            query_completa = f"{base_query} AND " + " AND ".join(filtros)
        else:
            query_completa = base_query

        result = db.execute(text(query_completa), parametros).fetchall()
        nombres = [row[0] for row in result]

        return {"nombres": nombres}

    except Exception as e:
        print("❌ ERROR EN CONSULTA:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

# ================================
# API DEL FORO - COMENTARIOS
# ================================

class ComentarioCreate(BaseModel):
    nombre: str
    tema: Optional[str] = None
    contenido: str

class ComentarioUpdate(BaseModel):
    contenido: str
    tema: Optional[str] = None

class ComentarioResponse(BaseModel):
    id: int
    nombre: str
    tema: Optional[str]
    contenido: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    likes: int

class TemaPopular(BaseModel):
    tema: str
    nombre_display: str
    contador: int

@app.get("/api/comentarios")
async def obtener_comentarios(
    db: Session = Depends(get_db),
    orden: str = Query("newest", regex="^(newest|oldest|popular)$"),
    tema: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    try:
        query = """
            SELECT id, nombre, tema, contenido, fecha_creacion, fecha_actualizacion, likes
            FROM comentarios_foro
            WHERE activo = true
        """
        
        params = {}
        
        if tema and tema != "all":
            query += " AND tema = :tema"
            params["tema"] = tema
        
        if orden == "newest":
            query += " ORDER BY fecha_creacion DESC"
        elif orden == "oldest":
            query += " ORDER BY fecha_creacion ASC"
        elif orden == "popular":
            query += " ORDER BY likes DESC, fecha_creacion DESC"
        
        query += " LIMIT :limit OFFSET :offset"
        params["limit"] = limit
        params["offset"] = offset
        
        result = db.execute(text(query), params).fetchall()
        
        comentarios = []
        for row in result:
            comentarios.append({
                "id": row[0],
                "nombre": row[1],
                "tema": row[2],
                "contenido": row[3],
                "fecha_creacion": row[4].isoformat(),
                "fecha_actualizacion": row[5].isoformat(),
                "likes": row[6]
            })
        
        count_query = "SELECT COUNT(*) FROM comentarios_foro WHERE activo = true"
        if tema and tema != "all":
            count_query += " AND tema = :tema"
        
        total = db.execute(text(count_query), {"tema": tema} if tema and tema != "all" else {}).scalar()
        
        return {
            "comentarios": comentarios,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
        
    except Exception as e:
        print(f"❌ Error al obtener comentarios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener comentarios")

@app.post("/api/comentarios", response_model=ComentarioResponse)
async def crear_comentario(
    comentario: ComentarioCreate,
    db: Session = Depends(get_db)
):
    try:
        nombre = comentario.nombre.strip()
        contenido = comentario.contenido.strip()
        
        if len(nombre) < 2:
            raise HTTPException(status_code=400, detail="El nombre debe tener al menos 2 caracteres")
        
        if len(contenido) < 10:
            raise HTTPException(status_code=400, detail="El comentario debe tener al menos 10 caracteres")
        
        if len(contenido) > 500:
            raise HTTPException(status_code=400, detail="El comentario no puede superar 500 caracteres")
        
        query = text("""
            INSERT INTO comentarios_foro (nombre, tema, contenido, fecha_creacion, fecha_actualizacion, likes, activo)
            VALUES (:nombre, :tema, :contenido, NOW(), NOW(), 0, true)
            RETURNING id, nombre, tema, contenido, fecha_creacion, fecha_actualizacion, likes
        """)
        
        result = db.execute(query, {
            "nombre": nombre,
            "tema": comentario.tema if comentario.tema and comentario.tema != "" else None,
            "contenido": contenido
        }).fetchone()
        
        db.commit()
        
        return {
            "id": result[0],
            "nombre": result[1],
            "tema": result[2],
            "contenido": result[3],
            "fecha_creacion": result[4],
            "fecha_actualizacion": result[5],
            "likes": result[6]
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear comentario: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/api/comentarios/{comentario_id}", response_model=ComentarioResponse)
async def actualizar_comentario(
    comentario_id: int,
    comentario: ComentarioUpdate,
    db: Session = Depends(get_db)
):
    try:
        if len(comentario.contenido.strip()) < 10:
            raise HTTPException(status_code=400, detail="El comentario debe tener al menos 10 caracteres")
        
        if len(comentario.contenido) > 500:
            raise HTTPException(status_code=400, detail="El comentario no puede superar 500 caracteres")
        
        check_query = text("SELECT id FROM comentarios_foro WHERE id = :id AND activo = true")
        exists = db.execute(check_query, {"id": comentario_id}).fetchone()
        
        if not exists:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        
        query = text("""
            UPDATE comentarios_foro
            SET contenido = :contenido, 
                tema = :tema,
                fecha_actualizacion = NOW()
            WHERE id = :id
            RETURNING id, nombre, tema, contenido, fecha_creacion, fecha_actualizacion, likes
        """)
        
        result = db.execute(query, {
            "id": comentario_id,
            "contenido": comentario.contenido.strip(),
            "tema": comentario.tema if comentario.tema and comentario.tema != "" else None
        }).fetchone()
        
        db.commit()
        
        return {
            "id": result[0],
            "nombre": result[1],
            "tema": result[2],
            "contenido": result[3],
            "fecha_creacion": result[4],
            "fecha_actualizacion": result[5],
            "likes": result[6]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al actualizar comentario: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el comentario")

@app.delete("/api/comentarios/{comentario_id}")
async def eliminar_comentario(
    comentario_id: int,
    db: Session = Depends(get_db)
):
    try:
        check_query = text("SELECT id, tema FROM comentarios_foro WHERE id = :id AND activo = true")
        comentario = db.execute(check_query, {"id": comentario_id}).fetchone()
        
        if not comentario:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        
        query = text("DELETE FROM comentarios_foro WHERE id = :id")
        db.execute(query, {"id": comentario_id})
        
        db.commit()
        
        return {"message": "Comentario eliminado correctamente", "id": comentario_id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al eliminar comentario: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el comentario")

@app.post("/api/comentarios/{comentario_id}/like")
async def dar_like(
    comentario_id: int,
    db: Session = Depends(get_db)
):
    try:
        check_query = text("SELECT id, likes FROM comentarios_foro WHERE id = :id AND activo = true")
        result = db.execute(check_query, {"id": comentario_id}).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        
        query = text("""
            UPDATE comentarios_foro
            SET likes = likes + 1
            WHERE id = :id
            RETURNING likes
        """)
        
        new_likes = db.execute(query, {"id": comentario_id}).scalar()
        db.commit()
        
        return {"likes": new_likes}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al dar like: {e}")
        raise HTTPException(status_code=500, detail="Error al dar like")

@app.get("/api/temas-populares", response_model=List[TemaPopular])
async def obtener_temas_populares(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=20)
):
    try:
        query = text("""
            SELECT tema, nombre_display, contador
            FROM temas_populares
            WHERE contador > 0
            ORDER BY contador DESC, ultima_actualizacion DESC
            LIMIT :limit
        """)
        
        result = db.execute(query, {"limit": limit}).fetchall()
        
        temas = []
        for row in result:
            temas.append({
                "tema": row[0],
                "nombre_display": row[1],
                "contador": row[2]
            })
        
        return temas
        
    except Exception as e:
        print(f"❌ Error al obtener temas populares: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener temas populares")

# ================================
# API DE PROGRAMAS ACADÉMICOS
# ================================

class AreaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    color_hex: str
    icono: Optional[str]

class ModalidadResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]

class UniversidadResponse(BaseModel):
    id: int
    nombre: str
    sigla: Optional[str]
    tipo_universidad: str

class ProgramaListResponse(BaseModel):
    id: int
    nombre: str
    universidad_id: int
    universidad_nombre: str
    universidad_sigla: Optional[str]
    universidad_website: str
    tipo_universidad: str
    ciudad: str
    departamento: str
    area_nombre: str
    area_color: str
    area_icono: Optional[str]
    duracion_semestres: int
    creditos: int
    modalidades: List[str]

class CampusDetail(BaseModel):
    id: int
    nombre: str
    direccion: str
    ciudad: Optional[str]
    telefono: Optional[str]
    es_principal: bool

class ProgramaDetailResponse(BaseModel):
    id: int
    nombre: str
    codigo_snies: Optional[str]
    universidad_id: int
    universidad_nombre: str
    universidad_sigla: Optional[str]
    universidad_website: str
    universidad_direccion: str
    universidad_telefono: str
    universidad_email: Optional[str]
    tipo_universidad: str
    ciudad: str
    departamento: str
    area_nombre: str
    area_color: str
    area_icono: Optional[str]
    duracion_semestres: int
    creditos: int
    titulo_otorgado: Optional[str]
    descripcion: Optional[str]
    perfil_profesional: Optional[str]
    campo_laboral: Optional[str]
    costo_semestre: Optional[float]
    modalidades: List[str]
    campus: List[CampusDetail]

@app.get("/api/programas", response_model=List[ProgramaListResponse])
async def get_programas(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT DISTINCT
                p.id,
                p.nombre,
                p.universidad_id,
                u.nombre as universidad_nombre,
                u.sigla as universidad_sigla,
                u.website as universidad_website,
                u.tipo_universidad,
                u.ciudad,
                u.departamento,
                a.nombre as area_nombre,
                a.color_hex as area_color,
                a.icono as area_icono,
                p.duracion_semestres,
                p.creditos,
                ARRAY_AGG(DISTINCT m.nombre) as modalidades
            FROM programas_academicos p
            INNER JOIN universidades u ON p.universidad_id = u.id
            LEFT JOIN areas_conocimiento a ON p.area_id = a.id
            LEFT JOIN programa_modalidades pm ON p.id = pm.programa_id
            LEFT JOIN modalidades m ON pm.modalidad_id = m.id
            WHERE p.activo = true AND u.activo = true
            GROUP BY p.id, p.nombre, p.universidad_id, u.nombre, u.sigla, u.website,
                     u.tipo_universidad, u.ciudad, u.departamento, a.nombre, 
                     a.color_hex, a.icono, p.duracion_semestres, p.creditos
            ORDER BY p.nombre
        """)
        
        result = db.execute(query).fetchall()
        
        programas = []
        for row in result:
            programas.append({
                "id": row[0],
                "nombre": row[1],
                "universidad_id": row[2],
                "universidad_nombre": row[3],
                "universidad_sigla": row[4],
                "universidad_website": row[5],
                "tipo_universidad": row[6],
                "ciudad": row[7],
                "departamento": row[8],
                "area_nombre": row[9] or "Sin área",
                "area_color": row[10] or "#95A5A6",
                "area_icono": row[11] or "📚",
                "duracion_semestres": row[12] or 0,
                "creditos": row[13] or 0,
                "modalidades": [m for m in row[14] if m] if row[14] else []
            })
        
        return programas
        
    except Exception as e:
        print(f"❌ Error al obtener programas: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener programas")

@app.get("/api/programas/{programa_id}", response_model=ProgramaDetailResponse)
async def get_programa_detail(programa_id: int, db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                p.id, p.nombre, p.codigo_snies, p.universidad_id,
                u.nombre, u.sigla, u.website, u.direccion, u.telefono, u.email,
                u.tipo_universidad, u.ciudad, u.departamento,
                a.nombre, a.color_hex, a.icono,
                p.duracion_semestres, p.creditos, p.titulo_otorgado,
                p.descripcion, p.perfil_profesional, p.campo_laboral, p.costo_semestre
            FROM programas_academicos p
            INNER JOIN universidades u ON p.universidad_id = u.id
            LEFT JOIN areas_conocimiento a ON p.area_id = a.id
            WHERE p.id = :programa_id AND p.activo = true
        """)
        
        result = db.execute(query, {"programa_id": programa_id}).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        
        modalidades_query = text("""
            SELECT m.nombre
            FROM programa_modalidades pm
            INNER JOIN modalidades m ON pm.modalidad_id = m.id
            WHERE pm.programa_id = :programa_id
        """)
        modalidades_result = db.execute(modalidades_query, {"programa_id": programa_id}).fetchall()
        modalidades = [row[0] for row in modalidades_result]
        
        campus_query = text("""
            SELECT DISTINCT c.id, c.nombre, c.direccion, c.ciudad, c.telefono, c.es_principal
            FROM programa_campus pc
            INNER JOIN campus c ON pc.campus_id = c.id
            WHERE pc.programa_id = :programa_id AND c.activo = true
        """)
        campus_result = db.execute(campus_query, {"programa_id": programa_id}).fetchall()
        campus = [
            {
                "id": row[0],
                "nombre": row[1],
                "direccion": row[2],
                "ciudad": row[3],
                "telefono": row[4],
                "es_principal": row[5]
            }
            for row in campus_result
        ]
        
        programa = {
            "id": result[0],
            "nombre": result[1],
            "codigo_snies": result[2],
            "universidad_id": result[3],
            "universidad_nombre": result[4],
            "universidad_sigla": result[5],
            "universidad_website": result[6],
            "universidad_direccion": result[7],
            "universidad_telefono": result[8],
            "universidad_email": result[9],
            "tipo_universidad": result[10],
            "ciudad": result[11],
            "departamento": result[12],
            "area_nombre": result[13] or "Sin área",
            "area_color": result[14] or "#95A5A6",
            "area_icono": result[15] or "📚",
            "duracion_semestres": result[16] or 0,
            "creditos": result[17] or 0,
            "titulo_otorgado": result[18],
            "descripcion": result[19],
            "perfil_profesional": result[20],
            "campo_laboral": result[21],
            "costo_semestre": float(result[22]) if result[22] else None,
            "modalidades": modalidades,
            "campus": campus
        }
        
        return programa
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error al obtener detalle del programa: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener detalle del programa")

@app.get("/api/universidades", response_model=List[UniversidadResponse])
async def get_universidades(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, nombre, sigla, tipo_universidad
            FROM universidades
            WHERE activo = true
            ORDER BY nombre
        """)
        
        result = db.execute(query).fetchall()
        
        universidades = [
            {
                "id": row[0],
                "nombre": row[1],
                "sigla": row[2],
                "tipo_universidad": row[3]
            }
            for row in result
        ]
        
        return universidades
        
    except Exception as e:
        print(f"❌ Error al obtener universidades: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener universidades")

@app.get("/api/areas", response_model=List[AreaResponse])
async def get_areas(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, nombre, descripcion, color_hex, icono
            FROM areas_conocimiento
            WHERE activo = true
            ORDER BY nombre
        """)
        
        result = db.execute(query).fetchall()
        
        areas = [
            {
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2],
                "color_hex": row[3],
                "icono": row[4]
            }
            for row in result
        ]
        
        return areas
        
    except Exception as e:
        print(f"❌ Error al obtener áreas: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener áreas")

@app.get("/api/modalidades", response_model=List[ModalidadResponse])
async def get_modalidades(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT id, nombre, descripcion
            FROM modalidades
            WHERE activo = true
            ORDER BY nombre
        """)
        
        result = db.execute(query).fetchall()
        
        modalidades = [
            {
                "id": row[0],
                "nombre": row[1],
                "descripcion": row[2]
            }
            for row in result
        ]
        
        return modalidades
        
    except Exception as e:
        print(f"❌ Error al obtener modalidades: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener modalidades")

def require_auth(request: Request) -> dict:
    """
    Requiere que el usuario esté autenticado.
    Lanza un error 401 si no lo está.
    """
    user = get_current_user(request)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Debes iniciar sesión para acceder a este recurso"
        )
    return user