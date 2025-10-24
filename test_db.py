from db import test_connection, SessionLocal, text

# Probar conexión básica
test_connection()

# Probar inserción de prueba
db = SessionLocal()
try:
    result = db.execute(text("SELECT COUNT(*) FROM usuarios"))
    print(f"✅ Usuarios en DB: {result.scalar()}")
    
    result = db.execute(text("SELECT COUNT(*) FROM tests_realizados"))
    print(f"✅ Tests en DB: {result.scalar()}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()