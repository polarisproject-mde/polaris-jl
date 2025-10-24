# db.py - Configuración OPTIMIZADA para Supabase

from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# 🔹 Cargar variables de entorno
load_dotenv()
URL_DATABASE = os.getenv("URL_DATABASE")

if not URL_DATABASE:
    raise ValueError("❌ La variable de entorno URL_DATABASE no está configurada")

print(f"🔗 Conectando a: {URL_DATABASE[:30]}...")  # Solo primeros 30 caracteres por seguridad

# 🔹 CONFIGURACIÓN CRÍTICA PARA SUPABASE
engine = create_engine(
    URL_DATABASE,
    echo=True,  # 🔥 CAMBIADO A TRUE PARA VER QUERIES SQL
    future=True,
    pool_size=3,
    max_overflow=2,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"
    },
    pool_timeout=20,
    pool_use_lifo=True
)

# 🔹 Configurar parámetros al conectar
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("SET SESSION statement_timeout = '30s'")
    cursor.execute("SET SESSION idle_in_transaction_session_timeout = '60s'")
    cursor.close()

# 🔹 Configuración de la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
    expire_on_commit=False
)

# 🔹 Dependencia OPTIMIZADA
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDepends = Annotated[Session, Depends(get_db)]

# 🔹 Función para verificar conexión
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a la base de datos")
            return True
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Probando conexión a la base de datos...")
    test_connection()