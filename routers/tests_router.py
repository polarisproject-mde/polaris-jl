# routers/tests_router.py - Router de Tests Vocacionales

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional
import json
from datetime import datetime

from db import get_db
from auth import get_current_user_session, get_current_user_hybrid

# ✅ CAMBIO: Importar desde tests_config en lugar de main
from tests_config import (
    TESTS_CONFIG,
    PUNTUACION_VALORES,
    calcular_resultados_test
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ================================
# RUTAS DE TESTS
# ================================

@router.get("/test-vocacional", response_class=HTMLResponse, name="test-vocacional")
async def test_vocacional(
    request: Request,
    user: dict = Depends(get_current_user_hybrid)
):
    """Página principal de tests vocacionales"""
    return templates.TemplateResponse(
        "test-vocacional.html",
        {"request": request, "user": user}
    )

@router.get("/test/{tipo_test}", response_class=HTMLResponse)
async def mostrar_test(
    request: Request,
    tipo_test: str,
    user: dict = Depends(get_current_user_hybrid)
):
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

@router.post("/test/{tipo_test}/procesar")
async def procesar_test(
    tipo_test: str,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    """Procesa las respuestas del test y las guarda"""
    try:
        # 1. Obtener respuestas
        form_data = await request.form()
        respuestas = {k: v for k, v in form_data.items() if k.startswith("pregunta_")}
        
        # 2. Validar completitud
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
        
        # 4. Guardar en base de datos (si está autenticado)
        test_id = None
        test_guardado = False
        
        if user:
            try:
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
                
                # 4.3 Guardar resultados detallados
                datos_adicionales = {
                    "perfil_identificado": resultados.get("perfil_identificado", ""),
                    "score_ajuste": float(resultados.get("score_ajuste", 0)),
                    "porcentaje_global": float(resultados.get("porcentaje_global", 0)),
                    "puntajes_dimensiones": resultados.get("puntajes_dimensiones", {})
                }
                
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
                
                db.commit()
                test_guardado = True
                
            except Exception as e:
                db.rollback()
                print(f"❌ ERROR al guardar test: {str(e)}")
                import traceback
                traceback.print_exc()
        
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
# RUTAS DE HISTORIAL
# ================================

@router.get("/mis-tests", response_class=HTMLResponse, name="resultados")
async def mis_tests(
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
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

@router.get("/test/{test_id}/detalle", response_class=HTMLResponse)
async def detalle_test(
    test_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    """Muestra el detalle de un test específico"""
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
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
            "puntajes_dimensiones": datos_adicionales.get("puntajes_dimensiones", {})
        }
        
        return templates.TemplateResponse(
            "resultado_test_detallado.html",
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

@router.delete("/test/{test_id}/eliminar")
async def eliminar_test(
    test_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
):
    """Elimina un test y todos sus datos relacionados"""
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        # Verificar que el test pertenece al usuario
        verify_query = text("""
            SELECT id FROM tests_realizados 
            WHERE id = :test_id AND usuario_id = :user_id
        """)
        
        test_exists = db.execute(verify_query, {
            "test_id": test_id,
            "user_id": user["id"]
        }).fetchone()
        
        if not test_exists:
            raise HTTPException(
                status_code=404, 
                detail="Test no encontrado o no tienes permiso para eliminarlo"
            )
        
        # Eliminar en orden (por las foreign keys)
        delete_respuestas = text("DELETE FROM respuestas_test WHERE test_id = :test_id")
        db.execute(delete_respuestas, {"test_id": test_id})
        
        delete_resultados = text("DELETE FROM resultados_test WHERE test_id = :test_id")
        db.execute(delete_resultados, {"test_id": test_id})
        
        delete_test = text("""
            DELETE FROM tests_realizados 
            WHERE id = :test_id AND usuario_id = :user_id
        """)
        db.execute(delete_test, {
            "test_id": test_id,
            "user_id": user["id"]
        })
        
        db.commit()
        
        print(f"✅ Test {test_id} eliminado correctamente")
        
        return {
            "success": True,
            "message": "Test eliminado correctamente",
            "test_id": test_id
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al eliminar test: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al eliminar el test: {str(e)}"
        )


# ================================
# API DE ANÁLISIS
# ================================

@router.get("/api/usuario/dimensiones")
async def get_dimensiones_usuario(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_hybrid)
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