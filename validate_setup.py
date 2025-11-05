# validate_setup.py - Script de validación de instalación

"""
Script para verificar que la instalación de v2.0 está correcta.
Ejecutar después de copiar todos los archivos.

Uso:
    python validate_setup.py
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_check(condition, message):
    """Imprime resultado de verificación"""
    symbol = "✅" if condition else "❌"
    print(f"{symbol} {message}")
    return condition

def validate_file_structure():
    """Valida que existan todos los archivos necesarios"""
    print_header("1. VALIDANDO ESTRUCTURA DE ARCHIVOS")
    
    required_files = {
        "main.py": "Archivo principal de la aplicación",
        "auth.py": "Sistema de autenticación JWT",
        "db.py": "Configuración de base de datos",
        "requirements.txt": "Dependencias del proyecto",
        ".env": "Variables de entorno",
    }
    
    required_dirs = {
        "routers": "Carpeta de routers modulares",
        "templates": "Plantillas HTML",
        "static": "Archivos estáticos",
    }
    
    router_files = {
        "routers/__init__.py": "Init del paquete routers",
        "routers/auth_router.py": "Router de autenticación",
        "routers/tests_router.py": "Router de tests",
        "routers/users_router.py": "Router de usuarios",
        "routers/foro_router.py": "Router del foro",
        "routers/programas_router.py": "Router de programas",
    }
    
    all_good = True
    
    # Verificar archivos raíz
    for file, desc in required_files.items():
        exists = os.path.exists(file)
        all_good = print_check(exists, f"{file} - {desc}") and all_good
    
    # Verificar directorios
    for dir, desc in required_dirs.items():
        exists = os.path.isdir(dir)
        all_good = print_check(exists, f"{dir}/ - {desc}") and all_good
    
    # Verificar archivos de routers
    for file, desc in router_files.items():
        exists = os.path.exists(file)
        all_good = print_check(exists, f"{file} - {desc}") and all_good
    
    return all_good

def validate_dependencies():
    """Valida que estén instaladas las dependencias necesarias"""
    print_header("2. VALIDANDO DEPENDENCIAS")
    
    dependencies = {
        "fastapi": "FastAPI framework",
        "uvicorn": "Servidor ASGI",
        "sqlalchemy": "ORM de base de datos",
        "psycopg2": "Driver PostgreSQL",
        "jose": "Librería JWT (python-jose)",
        "passlib": "Librería de hashing",
        "bcrypt": "Algoritmo bcrypt",
        "jinja2": "Motor de templates",
        "pydantic": "Validación de datos",
    }
    
    all_good = True
    
    for module, desc in dependencies.items():
        try:
            __import__(module)
            all_good = print_check(True, f"{module} - {desc}") and all_good
        except ImportError:
            all_good = print_check(False, f"{module} - {desc} (pip install {module})") and all_good
    
    return all_good

def validate_imports():
    """Valida que se puedan importar los módulos del proyecto"""
    print_header("3. VALIDANDO IMPORTACIONES DEL PROYECTO")
    
    imports = {
        "auth": ["get_current_user_jwt", "create_access_token", "get_password_hash"],
        "db": ["get_db", "SessionLocal"],
    }
    
    all_good = True
    
    for module, funcs in imports.items():
        try:
            imported = __import__(module)
            for func in funcs:
                has_func = hasattr(imported, func)
                all_good = print_check(has_func, f"{module}.{func}") and all_good
        except Exception as e:
            all_good = print_check(False, f"Error al importar {module}: {e}") and all_good
    
    # Validar importación de routers
    router_modules = [
        "routers.auth_router",
        "routers.tests_router",
        "routers.users_router",
        "routers.foro_router",
        "routers.programas_router",
    ]
    
    for router in router_modules:
        try:
            __import__(router)
            all_good = print_check(True, router) and all_good
        except Exception as e:
            all_good = print_check(False, f"Error al importar {router}: {e}") and all_good
    
    return all_good

def validate_env_variables():
    """Valida las variables de entorno"""
    print_header("4. VALIDANDO VARIABLES DE ENTORNO")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        print("⚠️  python-dotenv no instalado, omitiendo carga de .env")
    
    required_vars = {
        "URL_DATABASE": "URL de conexión a base de datos",
        "SECRET_KEY": "Clave secreta para sesiones",
        "JWT_SECRET_KEY": "Clave secreta para JWT",
    }
    
    optional_vars = {
        "ENVIRONMENT": "Entorno (development/production)",
    }
    
    all_good = True
    
    # Variables requeridas
    for var, desc in required_vars.items():
        value = os.getenv(var)
        exists = value is not None
        
        if exists:
            # Verificar que no sea un valor por defecto inseguro
            if var in ["SECRET_KEY", "JWT_SECRET_KEY"]:
                is_secure = len(value) >= 32 and not value.startswith("tu-")
                if not is_secure:
                    print_check(False, f"{var} - {desc} (⚠️  Usar clave más segura en producción)")
                    all_good = False
                else:
                    all_good = print_check(True, f"{var} - {desc}") and all_good
            else:
                all_good = print_check(True, f"{var} - {desc}") and all_good
        else:
            all_good = print_check(False, f"{var} - {desc} (NO CONFIGURADA)") and all_good
    
    # Variables opcionales
    for var, desc in optional_vars.items():
        value = os.getenv(var)
        exists = value is not None
        print_check(exists, f"{var} - {desc} (opcional)")
    
    return all_good

def validate_database_connection():
    """Valida la conexión a la base de datos"""
    print_header("5. VALIDANDO CONEXIÓN A BASE DE DATOS")
    
    try:
        from db import test_connection
        
        if test_connection():
            print_check(True, "Conexión a base de datos exitosa")
            return True
        else:
            print_check(False, "No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print_check(False, f"Error al probar conexión: {e}")
        return False

def validate_main_structure():
    """Valida que main.py tenga la estructura correcta"""
    print_header("6. VALIDANDO ESTRUCTURA DE MAIN.PY")
    
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = {
            "from routers import": "Importación de routers",
            "app.include_router": "Inclusión de routers",
            "SessionMiddleware": "Middleware de sesiones",
            "app.mount": "Montaje de archivos estáticos",
            "FastAPI": "Inicialización de FastAPI",
        }
        
        all_good = True
        for check, desc in checks.items():
            found = check in content
            all_good = print_check(found, desc) and all_good
        
        return all_good
        
    except Exception as e:
        print_check(False, f"Error al leer main.py: {e}")
        return False

def print_summary(results):
    """Imprime resumen de validación"""
    print_header("RESUMEN DE VALIDACIÓN")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\n📊 Resultados:")
    print(f"   ✅ Validaciones exitosas: {passed}/{total}")
    print(f"   ❌ Validaciones fallidas: {failed}/{total}")
    
    if all(results.values()):
        print("\n🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecutar: python main.py")
        print("   2. Abrir: http://localhost:8000")
        print("   3. Ver API docs: http://localhost:8000/docs")
        print("   4. (Opcional) Migrar contraseñas: python migrate_passwords.py")
        return 0
    else:
        print("\n⚠️  INSTALACIÓN INCOMPLETA")
        print("\n🔧 Acciones requeridas:")
        
        if not results["Estructura"]:
            print("   - Copiar todos los archivos necesarios")
        if not results["Dependencias"]:
            print("   - Ejecutar: pip install -r requirements.txt")
        if not results["Importaciones"]:
            print("   - Verificar que todos los archivos estén en su lugar")
        if not results["Variables de Entorno"]:
            print("   - Configurar archivo .env con todas las variables")
        if not results["Base de Datos"]:
            print("   - Verificar URL_DATABASE en .env")
        if not results["Main.py"]:
            print("   - Reemplazar main.py con la versión actualizada")
        
        print("\n📖 Consulta README.md para más información")
        return 1

def main():
    """Función principal"""
    print("\n" + "🔍" * 30)
    print("  VALIDACIÓN DE INSTALACIÓN v2.0")
    print("🔍" * 30)
    
    results = {
        "Estructura": validate_file_structure(),
        "Dependencias": validate_dependencies(),
        "Importaciones": validate_imports(),
        "Variables de Entorno": validate_env_variables(),
        "Base de Datos": validate_database_connection(),
        "Main.py": validate_main_structure(),
    }
    
    return print_summary(results)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)