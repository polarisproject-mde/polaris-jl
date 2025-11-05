# routers/auth_router.py - Router de Autenticación

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from auth import (
    authenticate_user,
    create_access_token,
    create_user,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    UserLogin,
    UserRegister,
    Token,
    get_current_user_session,
    get_current_user_jwt,
    update_user_password
)
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production" or os.getenv("VERCEL") is not None


# ================================
# API ENDPOINTS (JSON)
# ================================

@router.post("/api/auth/login", response_model=Token)
async def api_login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login vía API con JWT
    Retorna token de acceso
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "rol": user.rol},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "rol": user.rol
        }
    }

@router.post("/api/auth/register", response_model=Token)
async def api_register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Registro vía API con JWT
    Crea usuario y retorna token
    """
    # Verificar si el email ya existe
    check_query = text("SELECT id FROM usuarios WHERE gmail = :email")
    existing = db.execute(check_query, {"email": user_data.email}).fetchone()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email ya está registrado"
        )
    
    # Crear usuario
    try:
        new_user = create_user(db, user_data)
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user.id, "email": new_user.email, "rol": new_user.rol},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "nombre": new_user.nombre,
                "email": new_user.email,
                "rol": new_user.rol
            }
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )

@router.get("/api/auth/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user_jwt)
):
    """
    Obtiene información del usuario actual (requiere JWT)
    """
    return current_user

@router.post("/api/auth/change-password")
async def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    current_user: dict = Depends(get_current_user_jwt),
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña del usuario autenticado
    """
    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )
    
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    # Verificar contraseña actual
    from auth import get_user_by_email, verify_password
    user = get_user_by_email(db, current_user["gmail"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar contraseña actual (compatibilidad con sistema antiguo)
    if user.hashed_password.startswith("$2b$"):
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta"
            )
    else:
        if user.hashed_password != current_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta"
            )
    
    # Actualizar contraseña
    update_user_password(db, current_user["id"], new_password)
    
    return {"message": "Contraseña actualizada correctamente"}


# ================================
# WEB ENDPOINTS (HTML) - Compatibilidad
# ================================

@router.get("/login", response_class=HTMLResponse, name="login")
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_form(
    request: Request,
    Gmail: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Login tradicional con sesiones (mantener para compatibilidad)
    """
    try:
        # Buscar usuario
        query = text("SELECT id, nombre, gmail, rol FROM usuarios WHERE gmail = :gmail AND contraseña = :pwd")
        result = db.execute(query, {"gmail": Gmail, "pwd": contraseña}).fetchone()

        if result:
            # Guardar en sesión
            request.session.clear()
            request.session["user_id"] = result[0]
            request.session["user_nombre"] = result[1]
            request.session["user_gmail"] = result[2]
            request.session["user_rol"] = result[3]
            request.session["logged_in"] = True
            request.session["_force_save"] = True
            
            if IS_PRODUCTION:
                print(f"✅ Login PRODUCCIÓN - User: {result[1]}")
            
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Correo o contraseña incorrectos"}
            )
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Error al iniciar sesión. Intenta nuevamente."}
        )

@router.get("/register", response_class=HTMLResponse, name="register")
async def register_page(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register_form(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    rol: str = Form(...),
    contraseña: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Registro tradicional (mantener para compatibilidad)
    """
    try:
        # Verificar email existente
        check_query = text("SELECT * FROM usuarios WHERE gmail = :email")
        existing_user = db.execute(check_query, {"email": email}).fetchone()
        
        if existing_user:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Este correo ya está registrado"}
            )
        
        # Hashear contraseña
        hashed_pwd = get_password_hash(contraseña)
        
        # Insertar usuario
        insert_query = text("""
            INSERT INTO usuarios (nombre, gmail, rol, contraseña) 
            VALUES (:nombre, :email, :rol, :contraseña)
        """)
        
        db.execute(insert_query, {
            "nombre": nombre,
            "email": email,
            "rol": rol,
            "contraseña": hashed_pwd
        })
        db.commit()
        
        return RedirectResponse(url="/login", status_code=303)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al registrar: {e}")
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Error al crear la cuenta. Intenta de nuevo."}
        )

@router.get("/logout", name="logout")
async def logout(request: Request):
    """Logout tradicional"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)