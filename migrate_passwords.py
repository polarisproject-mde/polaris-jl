# migrate_passwords.py - Script para migrar contraseñas a bcrypt

"""
Script para migrar contraseñas existentes al sistema de hash bcrypt.
ADVERTENCIA: Este script modifica la base de datos. Hacer backup primero.

Uso:
    python migrate_passwords.py

El script:
1. Detecta contraseñas sin hashear (no empiezan con $2b$)
2. Las hashea con bcrypt
3. Actualiza la base de datos
4. Genera un reporte

Funcionalidad de rollback:
- Guarda un backup de contraseñas en passwords_backup.json
- Puedes restaurar con restore_passwords.py si algo sale mal
"""

from db import SessionLocal, text
from auth import get_password_hash
import json
from datetime import datetime

def backup_passwords():
    """Hace backup de todas las contraseñas antes de migrar"""
    db = SessionLocal()
    
    try:
        query = text("SELECT id, gmail, contraseña FROM usuarios")
        users = db.execute(query).fetchall()
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "users": [
                {
                    "id": user[0],
                    "email": user[1],
                    "password": user[2]
                }
                for user in users
            ]
        }
        
        with open("passwords_backup.json", "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup creado: passwords_backup.json ({len(backup_data['users'])} usuarios)")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False
    finally:
        db.close()

def migrate_passwords():
    """Migra todas las contraseñas sin hashear a bcrypt"""
    db = SessionLocal()
    
    try:
        # Obtener usuarios con contraseñas sin hashear
        query = text("SELECT id, gmail, contraseña FROM usuarios")
        users = db.execute(query).fetchall()
        
        migrated = 0
        already_hashed = 0
        errors = []
        
        print("\n🔄 Iniciando migración de contraseñas...\n")
        
        for user_id, email, pwd in users:
            try:
                # Verificar si ya está hasheada
                if pwd.startswith("$2b$"):
                    already_hashed += 1
                    print(f"⏭️  {email}: Ya hasheada, omitiendo")
                    continue
                
                # Hashear contraseña
                hashed_pwd = get_password_hash(pwd)
                
                # Actualizar en base de datos
                update_query = text("""
                    UPDATE usuarios 
                    SET contraseña = :pwd 
                    WHERE id = :id
                """)
                
                db.execute(update_query, {"pwd": hashed_pwd, "id": user_id})
                migrated += 1
                print(f"✅ {email}: Migrada correctamente")
                
            except Exception as e:
                errors.append({"email": email, "error": str(e)})
                print(f"❌ {email}: Error - {e}")
        
        # Hacer commit de todos los cambios
        if migrated > 0:
            confirm = input(f"\n¿Confirmar migración de {migrated} contraseñas? (si/no): ")
            if confirm.lower() in ['si', 's', 'yes', 'y']:
                db.commit()
                print(f"\n✅ Migración completada exitosamente!")
            else:
                db.rollback()
                print(f"\n❌ Migración cancelada. No se realizaron cambios.")
                return
        
        # Reporte final
        print("\n" + "="*50)
        print("📊 REPORTE DE MIGRACIÓN")
        print("="*50)
        print(f"✅ Contraseñas migradas: {migrated}")
        print(f"⏭️  Ya hasheadas: {already_hashed}")
        print(f"❌ Errores: {len(errors)}")
        print(f"📊 Total usuarios: {len(users)}")
        
        if errors:
            print("\n❌ Errores encontrados:")
            for err in errors:
                print(f"  - {err['email']}: {err['error']}")
        
        print("\n💡 Nota: El backup está en passwords_backup.json")
        print("   Si algo sale mal, ejecuta restore_passwords.py")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error crítico en migración: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

def verify_migration():
    """Verifica que todas las contraseñas estén hasheadas"""
    db = SessionLocal()
    
    try:
        query = text("SELECT COUNT(*) FROM usuarios WHERE contraseña NOT LIKE '$2b$%'")
        count = db.execute(query).scalar()
        
        if count == 0:
            print("\n✅ Verificación exitosa: Todas las contraseñas están hasheadas")
            return True
        else:
            print(f"\n⚠️  Advertencia: {count} contraseñas sin hashear encontradas")
            return False
            
    except Exception as e:
        print(f"\n❌ Error al verificar: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("="*50)
    print("🔐 MIGRACIÓN DE CONTRASEÑAS A BCRYPT")
    print("="*50)
    print("\nEste script convertirá todas las contraseñas")
    print("al formato seguro bcrypt.\n")
    
    # Paso 1: Crear backup
    print("📦 Paso 1: Creando backup de contraseñas...")
    if not backup_passwords():
        print("\n❌ No se pudo crear backup. Abortando por seguridad.")
        exit(1)
    
    # Paso 2: Migrar
    print("\n🔄 Paso 2: Migrando contraseñas...")
    migrate_passwords()
    
    # Paso 3: Verificar
    print("\n🔍 Paso 3: Verificando migración...")
    verify_migration()
    
    print("\n✅ Proceso completado!")