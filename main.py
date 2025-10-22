from fastapi import FastAPI, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional
from starlette.middleware.sessions import SessionMiddleware
import secrets

from db import get_db

app = FastAPI()

# 🔐 Agregar middleware de sesiones
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

# Configuración de templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🆕 CONFIGURACIÓN DE TESTS VOCACIONALES
TESTS_CONFIG = {
    "general": {
        "titulo": "Test Vocacional General",
        "descripcion": "Descubre tus áreas de interés profesional",
        "instrucciones": "Responde honestamente cada pregunta. No hay respuestas correctas o incorrectas.",
        "preguntas": [
            {
                "id": 1,
                "texto": "¿Disfrutas resolver problemas matemáticos y lógicos?",
                "opciones": [
                    {"valor": "A", "texto": "Totalmente de acuerdo"},
                    {"valor": "B", "texto": "De acuerdo"},
                    {"valor": "C", "texto": "Neutral"},
                    {"valor": "D", "texto": "En desacuerdo"},
                    {"valor": "E", "texto": "Totalmente en desacuerdo"}
                ]
            }
            # Aquí agregarías más preguntas...
        ]
    },
    "tecnologia": {
        "titulo": "Test de Tecnología",
        "descripcion": "Evalúa tu afinidad con carreras tecnológicas",
        "instrucciones": "Este test te ayudará a identificar si las carreras tecnológicas son para ti.",
        "preguntas": [
            {
                "id": 1,
                "texto": "¿Te interesa aprender lenguajes de programación?",
                "opciones": [
                    {"valor": "A", "texto": "Mucho"},
                    {"valor": "B", "texto": "Bastante"},
                    {"valor": "C", "texto": "Algo"},
                    {"valor": "D", "texto": "Poco"},
                    {"valor": "E", "texto": "Nada"}
                ]
            }
            # Más preguntas...
        ]
    },
    "ciencias": {
        "titulo": "Test de Ciencias",
        "descripcion": "Descubre tu vocación científica",
        "instrucciones": "Responde según tu interés real en actividades científicas.",
        "preguntas": [
            {
                "id": 1,
                "texto": "¿Te gusta realizar experimentos y descubrir cómo funcionan las cosas?",
                "opciones": [
                    {"valor": "A", "texto": "Totalmente de acuerdo"},
                    {"valor": "B", "texto": "De acuerdo"},
                    {"valor": "C", "texto": "Neutral"},
                    {"valor": "D", "texto": "En desacuerdo"},
                    {"valor": "E", "texto": "Totalmente en desacuerdo"}
                ]
            }
        ]
    },
    "ingenieria": {
        "titulo": "Test de Ingeniería",
        "descripcion": "Evalúa tu aptitud para carreras de ingeniería",
        "instrucciones": "Este test mide tu afinidad con el pensamiento ingenieril.",
        "preguntas": [
            {
                "id": 1,
                "texto": "¿Disfrutas diseñar y construir cosas?",
                "opciones": [
                    {"valor": "A", "texto": "Mucho"},
                    {"valor": "B", "texto": "Bastante"},
                    {"valor": "C", "texto": "Algo"},
                    {"valor": "D", "texto": "Poco"},
                    {"valor": "E", "texto": "Nada"}
                ]
            }
        ]
    },
    "economia": {
        "titulo": "Test de Economía",
        "descripcion": "Descubre tu afinidad con carreras económicas y de negocios",
        "instrucciones": "Responde según tu interés en temas económicos y financieros.",
        "preguntas": [
            {
                "id": 1,
                "texto": "¿Te interesa entender cómo funcionan los mercados y las finanzas?",
                "opciones": [
                    {"valor": "A", "texto": "Totalmente de acuerdo"},
                    {"valor": "B", "texto": "De acuerdo"},
                    {"valor": "C", "texto": "Neutral"},
                    {"valor": "D", "texto": "En desacuerdo"},
                    {"valor": "E", "texto": "Totalmente en desacuerdo"}
                ]
            }
        ]
    }
}

# 🆕 Función para obtener el usuario actual desde la sesión
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id:
        query = text("SELECT id, nombre, gmail, rol FROM usuarios WHERE id = :user_id")
        result = db.execute(query, {"user_id": user_id}).fetchone()
        if result:
            return {
                "id": result[0],
                "nombre": result[1],
                "gmail": result[2],
                "rol": result[3]
            }
    return None

# inicio
@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# blog
@app.get("/blog", response_class=HTMLResponse, name="blog")
async def blog(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("blog.html", {"request": request, "user": user})

# carreras demandadas
@app.get("/carrerasdem", response_class=HTMLResponse, name="carrerasdem")
async def carrerasdem(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("carrerasdem.html", {"request": request, "user": user})

# como elegir
@app.get("/comoelegir", response_class=HTMLResponse, name="comoelegir")
async def como_elegir(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("comoelegir.html", {"request": request, "user": user})

# errores comunes
@app.get("/errorescom", response_class=HTMLResponse, name="errorescom")
async def errores_comunes(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("errores.html", {"request": request, "user": user})

# fechas importantes
@app.get("/fechasimp", response_class=HTMLResponse, name="fechasimp")
async def fechas_importantes(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("fechasimp.html", {"request": request, "user": user})

# guia vocacional
@app.get("/guiav", response_class=HTMLResponse, name="guiav")
async def guia_vocacional(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("guiav.html", {"request": request, "user": user})

# mitos y realidades
@app.get("/mitosyr", response_class=HTMLResponse, name="mitosyr")
async def mitos_y_realidades(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("mitosyr.html", {"request": request, "user": user})

# profesiones
@app.get("/profesiones", response_class=HTMLResponse, name="profesiones")
async def profesiones(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("profesiones.html", {"request": request, "user": user})

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

        print("📘 SQL ejecutado:", query_completa)
        print("📗 Parámetros:", parametros)

        result = db.execute(text(query_completa), parametros).fetchall()
        nombres = [row[0] for row in result]
        print("✅ Resultado:", nombres)

        return {"nombres": nombres}

    except Exception as e:
        print("❌ ERROR EN CONSULTA:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
    
# recur y event
@app.get("/recuryevent", response_class=HTMLResponse, name="recuryevent")
async def recursos_eventos(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("recuryevent.html", {"request": request, "user": user})

# test-voca
@app.get("/test-vocacional", response_class=HTMLResponse, name="test-vocacional")
async def test_vocacional(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("test-vocacional.html", {"request": request, "user": user})

# 🆕 Ruta dinámica para cada tipo de test
@app.get("/test/{tipo_test}", response_class=HTMLResponse)
async def mostrar_test(request: Request, tipo_test: str, user: dict = Depends(get_current_user)):
    if tipo_test not in TESTS_CONFIG:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "mensaje": "Test no encontrado", "user": user}
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

# 🆕 Ruta para procesar resultados del test (POST)
@app.post("/test/{tipo_test}/resultado")
async def procesar_test(request: Request, tipo_test: str, user: dict = Depends(get_current_user)):
    form_data = await request.form()
    
    # Aquí procesarías las respuestas y calcularías el resultado
    respuestas = {}
    for key, value in form_data.items():
        respuestas[key] = value
    
    # TODO: Implementar lógica para calcular puntaje según el tipo de test
    # y guardar en la base de datos si el usuario está autenticado
    
    return templates.TemplateResponse(
        "resultado_test.html",
        {
            "request": request,
            "user": user,
            "tipo": tipo_test,
            "respuestas": respuestas
        }
    )

# universidades
@app.get("/universidades", response_class=HTMLResponse, name="universidades")
async def universidades(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("universidades.html", {"request": request, "user": user})

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

# 🆕 RUTAS PARA EL MENÚ DE USUARIO

# Perfil
@app.get("/perfil", response_class=HTMLResponse, name="perfil")
async def perfil(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("perfil.html", {"request": request, "user": user})

# Resultados del test
@app.get("/resultados", response_class=HTMLResponse, name="resultados")
async def resultados(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("resultados.html", {"request": request, "user": user})

# Actualizar información
@app.get("/actualizar-info", response_class=HTMLResponse, name="actualizar_info")
async def actualizar_info_get(request: Request, user: dict = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("actualizar_info.html", {"request": request, "user": user})

@app.post("/actualizar-info")
async def actualizar_info_post(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        update_query = text("""
            UPDATE usuarios 
            SET nombre = :nombre, gmail = :email 
            WHERE id = :user_id
        """)
        db.execute(update_query, {
            "nombre": nombre,
            "email": email,
            "user_id": user["id"]
        })
        db.commit()
        
        return RedirectResponse(url="/perfil", status_code=303)
    except Exception as e:
        db.rollback()
        print(f"❌ Error al actualizar: {e}")
        return templates.TemplateResponse(
            "actualizar_info.html",
            {"request": request, "user": user, "error": "Error al actualizar la información"}
        )

# Cerrar sesión
@app.get("/logout", name="logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# login - GET
@app.get("/login", response_class=HTMLResponse, name="login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# login - POST
@app.post("/login")
async def login_post(
    request: Request,
    Gmail: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    query = text("SELECT id, nombre, gmail, rol FROM usuarios WHERE gmail = :gmail AND contraseña = :pwd")
    result = db.execute(query, {"gmail": Gmail, "pwd": contraseña}).fetchone()

    if result:
        # 🔐 Guardar datos del usuario en la sesión
        request.session["user_id"] = result[0]
        request.session["user_nombre"] = result[1]
        request.session["user_gmail"] = result[2]
        request.session["user_rol"] = result[3]
        
        print(f"✅ Login exitoso: {result[1]} ({result[2]})")
        
        # Login correcto → redirige a /
        return RedirectResponse(url="/", status_code=303)
    else:
        # Login incorrecto → recarga la plantilla login.html COMPLETA
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Correo o contraseña incorrectos"}
        )

# register - GET
@app.get("/register", response_class=HTMLResponse, name="register")
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# register - POST
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
        # Verificar si el email ya existe
        check_query = text("SELECT * FROM usuarios WHERE gmail = :email")
        existing_user = db.execute(check_query, {"email": email}).fetchone()
        
        if existing_user:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Este correo ya está registrado"}
            )
        
        # Insertar el nuevo usuario
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
        
        print(f"✅ Usuario registrado: {nombre} - {email} - {rol}")
        
        # Registro exitoso → redirige al login
        return RedirectResponse(url="/login", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al registrar usuario: {e}")
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Error al crear la cuenta. Intenta de nuevo."}
        )