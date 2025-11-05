# routers/users_router.py - Router de Gestión de Usuarios

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from auth import (
    get_current_user_session,
    get_current_user_hybrid,
    get_password_hash,
    verify_password,
    get_user_by_email
)
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production" or os.getenv("VERCEL") is not None


# ================================
# RUTAS DE PERFIL
# ================================

@router.get("/perfil", response_class=HTMLResponse, name="perfil")
async def perfil(
    request: Request,
    user: dict = Depends(get_current_user_hybrid)
):
    """Página de perfil del usuario"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("perfil.html", {"request": request, "user": user})

@router.get("/actualizar-info", response_class=HTMLResponse, name="actualizar_info")
async def actualizar_info_get(
    request: Request,
    user: dict = Depends(get_current_user_hybrid)
):
    """Página para actualizar información del usuario"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("actualizar-info.html", {"request": request, "user": user})

@router.post("/actualizar-info")
async def actualizar_info_post(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    rol: str = Form(...),
    contraseña_actual: str = Form(None),
    contraseña_nueva: str = Form(None),
    contraseña_confirmar: str = Form(None),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    """Actualiza la información del usuario"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Verificar si el email ya está en uso
        check_email_query = text("SELECT id FROM usuarios WHERE gmail = :email AND id != :user_id")
        existing_user = db.execute(check_email_query, {"email": email, "user_id": user["id"]}).fetchone()
        
        if existing_user:
            return templates.TemplateResponse(
                "actualizar-info.html",
                {"request": request, "user": user, "error": "Este correo ya está en uso por otra cuenta"}
            )
        
        # Si quiere cambiar contraseña
        if contraseña_actual or contraseña_nueva or contraseña_confirmar:
            if not all([contraseña_actual, contraseña_nueva, contraseña_confirmar]):
                return templates.TemplateResponse(
                    "actualizar-info.html",
                    {"request": request, "user": user, "error": "Debes completar todos los campos de contraseña"}
                )
            
            # Verificar contraseña actual
            user_db = get_user_by_email(db, user["gmail"])
            
            if not user_db:
                return templates.TemplateResponse(
                    "actualizar-info.html",
                    {"request": request, "user": user, "error": "Error al verificar usuario"}
                )
            
            # Verificar contraseña actual (compatibilidad con sistema antiguo)
            if user_db.hashed_password.startswith("$2b$"):
                if not verify_password(contraseña_actual, user_db.hashed_password):
                    return templates.TemplateResponse(
                        "actualizar-info.html",
                        {"request": request, "user": user, "error": "La contraseña actual es incorrecta"}
                    )
            else:
                if user_db.hashed_password != contraseña_actual:
                    return templates.TemplateResponse(
                        "actualizar-info.html",
                        {"request": request, "user": user, "error": "La contraseña actual es incorrecta"}
                    )
            
            # Validar nueva contraseña
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
            
            # Actualizar con nueva contraseña
            hashed_pwd = get_password_hash(contraseña_nueva)
            update_query = text("""
                UPDATE usuarios 
                SET nombre = :nombre, gmail = :email, rol = :rol, contraseña = :nueva_pwd
                WHERE id = :user_id
            """)
            db.execute(update_query, {
                "nombre": nombre,
                "email": email,
                "rol": rol,
                "nueva_pwd": hashed_pwd,
                "user_id": user["id"]
            })
        else:
            # Actualizar sin cambiar contraseña
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
        
        # Actualizar sesión
        request.session["user_nombre"] = nombre
        request.session["user_gmail"] = email
        request.session["user_rol"] = rol
        request.session["_force_save"] = True
        
        # Actualizar objeto user local
        user["nombre"] = nombre
        user["gmail"] = email
        user["rol"] = rol
        
        return templates.TemplateResponse(
            "actualizar-info.html",
            {"request": request, "user": user, "success": "✅ Información actualizada correctamente"}
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al actualizar: {e}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse(
            "actualizar-info.html",
            {"request": request, "user": user, "error": "Error al actualizar la información"}
        )

@router.post("/eliminar-cuenta")
async def eliminar_cuenta(
    request: Request,
    contraseña: str = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    """Elimina la cuenta del usuario"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Verificar contraseña
        user_db = get_user_by_email(db, user["gmail"])
        
        if not user_db:
            return templates.TemplateResponse(
                "perfil.html",
                {"request": request, "user": user, "error": "Error al verificar usuario"}
            )
        
        # Verificar contraseña (compatibilidad)
        password_valid = False
        if user_db.hashed_password.startswith("$2b$"):
            password_valid = verify_password(contraseña, user_db.hashed_password)
        else:
            password_valid = (user_db.hashed_password == contraseña)
        
        if not password_valid:
            return templates.TemplateResponse(
                "perfil.html",
                {"request": request, "user": user, "error": "Contraseña incorrecta"}
            )
        
        # Eliminar usuario y todos sus datos (cascade)
        delete_query = text("DELETE FROM usuarios WHERE id = :user_id")
        db.execute(delete_query, {"user_id": user["id"]})
        db.commit()
        
        # Limpiar sesión
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
# API DE INFORMACIÓN DE USUARIO
# ================================

@router.get("/api/usuario/info")
async def get_user_info(
    user: dict = Depends(get_current_user_hybrid)
):
    """Obtiene información del usuario actual"""
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    return {
        "id": user["id"],
        "nombre": user["nombre"],
        "email": user["gmail"],
        "rol": user["rol"]
    }

@router.get("/api/usuario/estadisticas")
async def get_user_stats(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    """Obtiene estadísticas del usuario"""
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        # Contar tests realizados
        query_tests = text("""
            SELECT COUNT(*) FROM tests_realizados 
            WHERE usuario_id = :user_id AND completado = true
        """)
        total_tests = db.execute(query_tests, {"user_id": user["id"]}).scalar()
        
        # Obtener test más reciente
        query_recent = text("""
            SELECT tipo_test, fecha_realizacion
            FROM tests_realizados
            WHERE usuario_id = :user_id AND completado = true
            ORDER BY fecha_realizacion DESC
            LIMIT 1
        """)
        recent_test = db.execute(query_recent, {"user_id": user["id"]}).fetchone()
        
        # Obtener área más fuerte
        query_area = text("""
            SELECT r.area_principal, COUNT(*) as veces
            FROM tests_realizados t
            INNER JOIN resultados_test r ON t.id = r.test_id
            WHERE t.usuario_id = :user_id
            GROUP BY r.area_principal
            ORDER BY veces DESC
            LIMIT 1
        """)
        top_area = db.execute(query_area, {"user_id": user["id"]}).fetchone()
        
        return {
            "total_tests": total_tests or 0,
            "ultimo_test": {
                "tipo": recent_test[0] if recent_test else None,
                "fecha": recent_test[1].isoformat() if recent_test else None
            } if recent_test else None,
            "area_mas_fuerte": top_area[0] if top_area else None
        }
        
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener estadísticas")