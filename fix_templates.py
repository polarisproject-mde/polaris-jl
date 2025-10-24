#!/usr/bin/env python3
"""
Script para corregir todas las referencias a archivos estáticos en templates
Reemplaza url_for('static', ...) por rutas absolutas /static/...
"""

import re
import os
from pathlib import Path

def fix_static_urls(content):
    """Reemplaza url_for de archivos estáticos por rutas absolutas"""
    
    # Pattern 1: {{ url_for('static', path='css/file.css') }}
    pattern1 = r"{{\s*url_for\('static',\s*path='([^']+)'\)\s*}}"
    content = re.sub(pattern1, r"/static/\1", content)
    
    # Pattern 2: {{ url_for('static', path="css/file.css") }}
    pattern2 = r'{{\s*url_for\("static",\s*path="([^"]+)"\)\s*}}'
    content = re.sub(pattern2, r'/static/\1', content)
    
    return content

def process_templates_directory(templates_dir="templates"):
    """Procesa todos los archivos HTML en el directorio templates"""
    
    templates_path = Path(templates_dir)
    
    if not templates_path.exists():
        print(f"❌ Directorio {templates_dir} no encontrado")
        return
    
    html_files = list(templates_path.glob("*.html"))
    
    print(f"📁 Encontrados {len(html_files)} archivos HTML")
    
    for html_file in html_files:
        print(f"\n🔄 Procesando: {html_file.name}")
        
        try:
            # Leer contenido
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Contar reemplazos
            original_content = content
            content = fix_static_urls(content)
            
            # Verificar si hubo cambios
            if content != original_content:
                # Guardar archivo modificado
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Contar número de cambios
                changes = len(re.findall(r'/static/', content)) - len(re.findall(r'/static/', original_content))
                print(f"   ✅ {changes} rutas corregidas")
            else:
                print(f"   ℹ️ Sin cambios necesarios")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando corrección de rutas estáticas en templates...\n")
    process_templates_directory()
    print("\n✅ Proceso completado")