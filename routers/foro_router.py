# routers/foro_router.py - Router del Foro de Comentarios

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel

from db import get_db

router = APIRouter()


# ================================
# MODELOS PYDANTIC
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
    fecha_creacion: str
    fecha_actualizacion: str
    likes: int

class TemaPopular(BaseModel):
    tema: str
    nombre_display: str
    contador: int


# ================================
# ENDPOINTS DE COMENTARIOS
# ================================

@router.get("/api/comentarios")
async def obtener_comentarios(
    db: Session = Depends(get_db),
    orden: str = Query("newest", regex="^(newest|oldest|popular)$"),
    tema: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Obtiene comentarios del foro con filtros y paginación"""
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

@router.post("/api/comentarios", response_model=ComentarioResponse)
async def crear_comentario(
    comentario: ComentarioCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo comentario en el foro"""
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
            "fecha_creacion": result[4].isoformat(),
            "fecha_actualizacion": result[5].isoformat(),
            "likes": result[6]
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear comentario: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/api/comentarios/{comentario_id}", response_model=ComentarioResponse)
async def actualizar_comentario(
    comentario_id: int,
    comentario: ComentarioUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un comentario existente"""
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
            "fecha_creacion": result[4].isoformat(),
            "fecha_actualizacion": result[5].isoformat(),
            "likes": result[6]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error al actualizar comentario: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el comentario")

@router.delete("/api/comentarios/{comentario_id}")
async def eliminar_comentario(
    comentario_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un comentario del foro"""
    try:
        check_query = text("SELECT id FROM comentarios_foro WHERE id = :id AND activo = true")
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

@router.post("/api/comentarios/{comentario_id}/like")
async def dar_like(
    comentario_id: int,
    db: Session = Depends(get_db)
):
    """Da like a un comentario"""
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

@router.get("/api/temas-populares", response_model=List[TemaPopular])
async def obtener_temas_populares(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=20)
):
    """Obtiene los temas más populares del foro"""
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