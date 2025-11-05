# routers/programas_router.py - Router de Programas Académicos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from db import get_db

router = APIRouter()


# ================================
# MODELOS PYDANTIC
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


# ================================
# ENDPOINTS DE PROGRAMAS
# ================================

@router.get("/api/programas", response_model=List[ProgramaListResponse])
async def get_programas(db: Session = Depends(get_db)):
    """Obtiene lista de todos los programas académicos"""
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

@router.get("/api/programas/{programa_id}", response_model=ProgramaDetailResponse)
async def get_programa_detail(programa_id: int, db: Session = Depends(get_db)):
    """Obtiene detalle completo de un programa académico"""
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
        
        # Obtener modalidades
        modalidades_query = text("""
            SELECT m.nombre
            FROM programa_modalidades pm
            INNER JOIN modalidades m ON pm.modalidad_id = m.id
            WHERE pm.programa_id = :programa_id
        """)
        modalidades_result = db.execute(modalidades_query, {"programa_id": programa_id}).fetchall()
        modalidades = [row[0] for row in modalidades_result]
        
        # Obtener campus
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

@router.get("/api/universidades", response_model=List[UniversidadResponse])
async def get_universidades(db: Session = Depends(get_db)):
    """Obtiene lista de universidades"""
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

@router.get("/api/areas", response_model=List[AreaResponse])
async def get_areas(db: Session = Depends(get_db)):
    """Obtiene lista de áreas de conocimiento"""
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

@router.get("/api/modalidades", response_model=List[ModalidadResponse])
async def get_modalidades(db: Session = Depends(get_db)):
    """Obtiene lista de modalidades de estudio"""
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


# ================================
# ENDPOINTS DE BÚSQUEDA Y FILTROS
# ================================

@router.get("/api/filtrar-carreras")
async def filtrar_carreras(
    db: Session = Depends(get_db),
    area: Optional[str] = None,
    modalidad: Optional[str] = None,
    duracion: Optional[str] = None,
    especializacion: Optional[str] = None
):
    """Filtra carreras según criterios"""
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
        raise HTTPException(status_code=500, detail=str(e))