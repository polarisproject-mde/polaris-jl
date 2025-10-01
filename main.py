from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db  # 👈 CAMBIAMOS ESTO

app = FastAPI()

# Configuración de templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/blog", response_class=HTMLResponse, name="blog")
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})

@app.get("/quienes-somos", response_class=HTMLResponse, name="quienes_somos")
async def quienes_somos(request: Request):
    return templates.TemplateResponse("quienes_somos.html", {"request": request})

@app.get("/carrerasdem", response_class=HTMLResponse, name="carrerasdem")
async def carrerasdem(request: Request):
    return templates.TemplateResponse("carrerasdem.html", {"request": request})

@app.get("/comoelegir", response_class=HTMLResponse, name="comoelegir")
async def como_elegir(request: Request):
    return templates.TemplateResponse("comoelegir.html", {"request": request})

@app.get("/errorescom", response_class=HTMLResponse, name="errorescom")
async def errores_comunes(request: Request):
    return templates.TemplateResponse("errores.html", {"request": request})

@app.get("/fechasimp", response_class=HTMLResponse, name="fechasimp")
async def fechas_importantes(request: Request):
    return templates.TemplateResponse("fechasimp.html", {"request": request})

@app.get("/guiav", response_class=HTMLResponse, name="guiav")
async def guia_vocacional(request: Request):
    return templates.TemplateResponse("guiav.html", {"request": request})

@app.get("/mitosyr", response_class=HTMLResponse, name="mitosyr")
async def mitos_y_realidades(request: Request):
    return templates.TemplateResponse("mitosyr.html", {"request": request})

@app.get("/profesiones", response_class=HTMLResponse, name="profesiones")
async def profesiones(request: Request):
    return templates.TemplateResponse("profesiones.html", {"request": request})

@app.get("/recuryevent", response_class=HTMLResponse, name="recuryevent")
async def recursos_eventos(request: Request):
    return templates.TemplateResponse("recuryevent.html", {"request": request})

@app.get("/test-vocacional", response_class=HTMLResponse, name="test-vocacional")
async def test_vocacional(request: Request):
    return templates.TemplateResponse("test-vocacional.html", {"request": request})

@app.get("/test", response_class=HTMLResponse, name="test")
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/test-cienc", response_class=HTMLResponse, name="test_cienc")
async def test_ciencias(request: Request):
    return templates.TemplateResponse("test_cienc.html", {"request": request})

@app.get("/test-eco", response_class=HTMLResponse, name="test_eco")
async def test_economia(request: Request):
    return templates.TemplateResponse("test_eco.html", {"request": request})

@app.get("/test-ing", response_class=HTMLResponse, name="test_ing")
async def test_ingenieria(request: Request):
    return templates.TemplateResponse("test_ing.html", {"request": request})

@app.get("/test-tecn", response_class=HTMLResponse, name="test_tecn")
async def test_tecnologia(request: Request):
    return templates.TemplateResponse("test_tecn.html", {"request": request})

@app.get("/universidades", response_class=HTMLResponse, name="universidades")
async def universidades(request: Request):
    return templates.TemplateResponse("universidades.html", {"request": request})

@app.get("/login", response_class=HTMLResponse, name="login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login_post(
    request: Request,
    Gmail: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)  # 👈 CAMBIAMOS ESTO
):
    query = text("SELECT * FROM usuarios WHERE Gmail = :gmail AND contraseña = :pwd")
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