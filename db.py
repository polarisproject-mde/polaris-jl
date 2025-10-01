from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# 🔹 Cargar variables de entorno
load_dotenv()
URL_DATABASE = os.getenv("URL_DATABASE")

if not URL_DATABASE:
    raise ValueError("❌ La variable de entorno URL_DATABASE no está configurada")

# 🔹 Crear motor de conexión
engine = create_engine(URL_DATABASE, echo=False, future=True)

# 🔹 Probar conexión (solo para desarrollo)
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa")
except Exception as e:
    print(f"❌ Error de conexión a la base de datos: {e}")

# 🔹 Configuración de la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# 🔹 Dependencia para inyectar la sesión en los endpoints
def get_db():
    with SessionLocal() as session:
        yield session

# 🔹 Atajo para usar en las rutas
SessionDepends = Annotated[Session, Depends(get_db)]
