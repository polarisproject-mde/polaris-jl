# restore_passwords.py - Script para restaurar contraseñas desde backup

"""
Script de emergencia para restaurar contraseñas desde el backup.
Solo usar si la migración falló o causó problemas.

Uso:
    python restore_passwords.py

Requiere: passwords_backup.json (generado por migrate_passwords.py)
"""

from db import SessionLocal, text
import json
from datetime import datetime
import os

def restore_passwords():
    """Restaura contraseñas desde el archivo de backup"""
    
    # Verificar que existe el backup
    if not os.path.exists("passwords_backup.json"):
        print("❌ Error: No se encontró passwords_backup.json")
        print("   El backup debe estar en el mismo directorio que este script.")
        return False
    
    # Leer backup
    try:
        with open("passwords_backup.json", "r", encoding="utf-8") as f:
            backup_data = json.load(f)
    except Exception as e:
        print(f"❌ Error al leer backup: {e}")
        return False
    
    # Mostrar información del backup
    print("\n📦 INFORMACIÓN DEL BACKUP")
    print("="*50)
    print(f"Fecha: {backup_data['timestamp']}")
    print(f"Usuarios en backup: {len(backup_data['users'])}")
    
    # Confirmar restauración
    print("\n⚠️  ADVERTENCIA: Esta acción sobrescribirá las contraseñas actuales")
    confirm = input("¿Continuar con la restauración? (si/no): ")
    
    if confirm.lower() not in ['si', 's', 'yes', 'y']:
        print("\n❌ Restauración cancelada.")
        return False
    
    db = SessionLocal()
    
    try:
        restored = 0
        not_found = []
        errors = []
        
        print("\n🔄 Restaurando contraseñas...\n")
        
        for user in backup_data['users']:
            try:
                # Verificar que el usuario existe
                check_query = text("SELECT id FROM usuarios WHERE id = :id")
                exists = db.execute(check_query, {"id": user['id']}).fetchone()
                
                if not exists:
                    not_found.append(user['email'])
                    print(f"⚠️  {user['email']}: Usuario no encontrado, omitiendo")
                    continue
                
                # Restaurar contraseña
                update_query = text("""
                    UPDATE usuarios 
                    SET contraseña = :pwd 
                    WHERE id = :id
                """)
                
                db.execute(update_query, {
                    "pwd": user['password'],
                    "id": user['id']
                })
                
                restored += 1
                print(f"✅ {user['email']}: Restaurada")
                
            except Exception as e:
                errors.append({"email": user['email'], "error": str(e)})
                print(f"❌ {user['email']}: Error - {e}")
        
        # Confirmar cambios
        if restored > 0:
            confirm_commit = input(f"\n¿Confirmar restauración de {restored} contraseñas? (si/no): ")
            if confirm_commit.lower() in ['si', 's', 'yes', 'y']:
                db.commit()
                print(f"\n✅ Restauración completada!")
            else:
                db.rollback()
                print(f"\n❌ Restauración cancelada. No se realizaron cambios.")
                return False
        
        # Reporte final
        print("\n" + "="*50)
        print("📊 REPORTE DE RESTAURACIÓN")
        print("="*50)
        print(f"✅ Contraseñas restauradas: {restored}")
        print(f"⚠️  Usuarios no encontrados: {len(not_found)}")
        print(f"❌ Errores: {len(errors)}")
        print(f"📊 Total en backup: {len(backup_data['users'])}")
        
        if not_found:
            print("\n⚠️  Usuarios no encontrados:")
            for email in not_found:
                print(f"  - {email}")
        
        if errors:
            print("\n❌ Errores encontrados:")
            for err in errors:
                print(f"  - {err['email']}: {err['error']}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error crítico en restauración: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

def create_new_backup():
    """Crea un backup de seguridad antes de restaurar"""
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
        
        filename = f"passwords_backup_pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup actual creado: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear backup actual: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("="*50)
    print("🔙 RESTAURACIÓN DE CONTRASEÑAS DESDE BACKUP")
    print("="*50)
    
    # Crear backup del estado actual antes de restaurar
    print("\n📦 Creando backup del estado actual...")
    create_new_backup()
    
    # Restaurar
    print("\n🔄 Iniciando restauración desde backup...")
    if restore_passwords():
        print("\n✅ Restauración completada exitosamente!")
    else:
        print("\n❌ Restauración fallida o cancelada.")