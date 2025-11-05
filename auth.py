# auth.py - Sistema de Autenticación JWT

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import os

from db import get_db

# ================================
# CONFIGURACIÓN
# ================================

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "tu-super-secreto-cambiar-en-produccion-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 días

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme para JWT
security = HTTPBearer()


# ================================
# MODELOS PYDANTIC
# ================================

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    rol: str
    password: str

class UserInDB(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    hashed_password: str


# ================================
# FUNCIONES DE UTILIDAD
# ================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña coincida con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def decode_access_token(token: str) -> TokenData:
    """Decodifica y valida un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        return TokenData(user_id=user_id, email=email)
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )


# ================================
# FUNCIONES DE AUTENTICACIÓN
# ================================

def get_user_by_email(db: Session, email: str) -> Optional[UserInDB]:
    """Obtiene usuario por email"""
    try:
        query = text("""
            SELECT id, nombre, gmail, rol, contraseña
            FROM usuarios
            WHERE gmail = :email
        """)
        result = db.execute(query, {"email": email}).fetchone()
        
        if result:
            return UserInDB(
                id=result[0],
                nombre=result[1],
                email=result[2],
                rol=result[3],
                hashed_password=result[4]
            )
        return None
    
    except Exception as e:
        print(f"❌ Error al obtener usuario: {e}")
        return None

def authenticate_user(db: Session, email: str, password: str) -> Optional[UserInDB]:
    """Autentica usuario con email y contraseña"""
    user = get_user_by_email(db, email)
    
    if not user:
        return None
    
    # Si la contraseña en DB no está hasheada (compatibilidad con sistema antiguo)
    if not user.hashed_password.startswith("$2b$"):
        # Comparación directa (sistema antiguo)
        if user.hashed_password == password:
            return user
        return None
    
    # Verificar contraseña hasheada
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


# ================================
# DEPENDENCIAS DE FASTAPI
# ================================

async def get_current_user_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> dict:
    """
    Obtiene el usuario actual desde el token JWT.
    Uso: user = Depends(get_current_user_jwt)
    """
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    user = get_user_by_email(db, token_data.email)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return {
        "id": user.id,
        "nombre": user.nombre,
        "gmail": user.email,
        "rol": user.rol
    }

async def get_current_user_optional_jwt(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    Obtiene el usuario actual si existe token, sino retorna None.
    Compatible con páginas públicas.
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    try:
        token = auth_header.split(" ")[1]
        token_data = decode_access_token(token)
        user = get_user_by_email(db, token_data.email)
        
        if user:
            return {
                "id": user.id,
                "nombre": user.nombre,
                "gmail": user.email,
                "rol": user.rol
            }
    except:
        return None
    
    return None


# ================================
# FUNCIONES DE SESIÓN (COMPATIBILIDAD)
# ================================

def get_current_user_session(request: Request) -> Optional[dict]:
    """
    Obtiene usuario desde sesión (sistema antiguo).
    Mantener para compatibilidad con templates.
    """
    user_id = request.session.get("user_id")
    
    if not user_id:
        return None
    
    return {
        "id": user_id,
        "nombre": request.session.get("user_nombre"),
        "gmail": request.session.get("user_gmail"),
        "rol": request.session.get("user_rol")
    }

def get_current_user_hybrid(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[dict]:
    """
    Sistema híbrido: intenta JWT primero, luego sesión.
    Permite transición gradual al nuevo sistema.
    """
    # Intentar JWT
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            token_data = decode_access_token(token)
            user = get_user_by_email(db, token_data.email)
            
            if user:
                return {
                    "id": user.id,
                    "nombre": user.nombre,
                    "gmail": user.email,
                    "rol": user.rol
                }
        except:
            pass
    
    # Fallback a sesión
    return get_current_user_session(request)


# ================================
# FUNCIONES DE UTILIDAD ADICIONALES
# ================================

def create_user(db: Session, user_data: UserRegister) -> UserInDB:
    """Crea un nuevo usuario con contraseña hasheada"""
    hashed_pwd = get_password_hash(user_data.password)
    
    query = text("""
        INSERT INTO usuarios (nombre, gmail, rol, contraseña)
        VALUES (:nombre, :email, :rol, :password)
        RETURNING id, nombre, gmail, rol, contraseña
    """)
    
    result = db.execute(query, {
        "nombre": user_data.nombre,
        "email": user_data.email,
        "rol": user_data.rol,
        "password": hashed_pwd
    }).fetchone()
    
    db.commit()
    
    return UserInDB(
        id=result[0],
        nombre=result[1],
        email=result[2],
        rol=result[3],
        hashed_password=result[4]
    )

def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
    """Actualiza la contraseña de un usuario"""
    hashed_pwd = get_password_hash(new_password)
    
    query = text("""
        UPDATE usuarios
        SET contraseña = :password
        WHERE id = :user_id
    """)
    
    db.execute(query, {"password": hashed_pwd, "user_id": user_id})
    db.commit()
    
    return True