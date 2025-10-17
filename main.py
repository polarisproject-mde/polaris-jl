from fastapi import FastAPI, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse # 👈 NUEVA IMPORTACIÓN: JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional # 👈 NUEVA IMPORTACIÓN

from db import get_db  # 👈 CAMBIAMOS ESTO

app = FastAPI()

# Configuración de templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# inicio
@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# blog
@app.get("/blog", response_class=HTMLResponse, name="blog")
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})

# Somos
@app.get("/quienes-somos", response_class=HTMLResponse, name="quienes_somos")
async def quienes_somos(request: Request):
    return templates.TemplateResponse("quienes_somos.html", {"request": request})

# carreras demandadas
@app.get("/carrerasdem", response_class=HTMLResponse, name="carrerasdem")
async def carrerasdem(request: Request):
    return templates.TemplateResponse("carrerasdem.html", {"request": request})

# como elegir
@app.get("/comoelegir", response_class=HTMLResponse, name="comoelegir")
async def como_elegir(request: Request):
    return templates.TemplateResponse("comoelegir.html", {"request": request})

# errores comunes
@app.get("/errorescom", response_class=HTMLResponse, name="errorescom")
async def errores_comunes(request: Request):
    return templates.TemplateResponse("errores.html", {"request": request})

# fechas importantes
@app.get("/fechasimp", response_class=HTMLResponse, name="fechasimp")
async def fechas_importantes(request: Request):
    return templates.TemplateResponse("fechasimp.html", {"request": request})

# guia vocacional
@app.get("/guiav", response_class=HTMLResponse, name="guiav")
async def guia_vocacional(request: Request):
    return templates.TemplateResponse("guiav.html", {"request": request})

# mitos y realidades
@app.get("/mitosyr", response_class=HTMLResponse, name="mitosyr")
async def mitos_y_realidades(request: Request):
    return templates.TemplateResponse("mitosyr.html", {"request": request})

# profesiones
@app.get("/profesiones", response_class=HTMLResponse, name="profesiones")
async def profesiones(request: Request):
    return templates.TemplateResponse("profesiones.html", {"request": request})

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
async def recursos_eventos(request: Request):
    return templates.TemplateResponse("recuryevent.html", {"request": request})

# test-voca
@app.get("/test-vocacional", response_class=HTMLResponse, name="test-vocacional")
async def test_vocacional(request: Request):
    return templates.TemplateResponse("test-vocacional.html", {"request": request})

# test
@app.get("/test", response_class=HTMLResponse, name="test")
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

# test_cienc
@app.get("/test-cienc", response_class=HTMLResponse, name="test_cienc")
async def test_ciencias(request: Request):
    return templates.TemplateResponse("test_cienc.html", {"request": request})

# test_eco
@app.get("/test-eco", response_class=HTMLResponse, name="test_eco")
async def test_economia(request: Request):
    return templates.TemplateResponse("test_eco.html", {"request": request})

# test_ing
@app.get("/test-ing", response_class=HTMLResponse, name="test_ing")
async def test_ingenieria(request: Request):
    return templates.TemplateResponse("test_ing.html", {"request": request})

# test-tecn
@app.get("/test-tecn", response_class=HTMLResponse, name="test_tecn")
async def test_tecnologia(request: Request):
    return templates.TemplateResponse("test_tecn.html", {"request": request})

# universidades
@app.get("/universidades", response_class=HTMLResponse, name="universidades")
async def universidades(request: Request):
    return templates.TemplateResponse("universidades.html", {"request": request})

@app.get("/articulos", response_class=HTMLResponse, name="articulos")
async def universidades(request: Request):
    return templates.TemplateResponse("articulos.html", {"request": request})

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
    query = text("SELECT * FROM usuarios WHERE gmail = :gmail AND contraseña = :pwd")
    result = db.execute(query, {"gmail": Gmail, "pwd": contraseña}).fetchone()

    if result:
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