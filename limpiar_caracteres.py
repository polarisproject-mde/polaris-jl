# Limpia caracteres raros del archivo main.py
with open('main.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

for c in ['ð', 'Ã', 'â', '¡', '­']:
    content = content.replace(c, '')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Archivo limpiado correctamente.")
