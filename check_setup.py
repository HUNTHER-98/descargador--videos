 #!/usr/bin/env python3
"""
Script de diagnóstico - Verifica que todo está configurado para descargas de YouTube
"""

import os
import sys

def check_environment():
    """Verifica el ambiente"""
    print("🔍 Verificando Ambiente...")
    print("-" * 50)
    
    # Verificar Python
    print(f"✅ Python: {sys.version}")
    
    # Verificar paquetes
    packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'yt_dlp': 'yt-dlp',
        'browser_cookie3': 'browser-cookie3',
    }
    
    print("\n📦 Paquetes instalados:")
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - FALTA INSTALAR")
            print(f"     pip install {name.lower().replace(' ', '-')}")
    
    # Verificar carpetas
    print("\n📁 Carpetas:")
    if os.path.exists('downloads'):
        print("  ✅ Carpeta downloads existe")
    else:
        print("  ⚠️  Carpeta downloads no existe (se creará automáticamente)")
    
    # Verificar cookies
    print("\n🍪 Cookies:")
    if os.path.exists('cookies.txt'):
        print("  ✅ Archivo cookies.txt encontrado")
    else:
        print("  ℹ️  cookies.txt no encontrado (se intentará obtener del navegador)")
    
    # Verificar archivos
    print("\n📄 Archivos:")
    files = ['server.py', 'app.py', 'index.html', 'requirements.txt']
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} no encontrado")
    
    print("\n" + "-" * 50)
    print("✅ Verificación completada")
    print("\nPasos siguientes:")
    print("1. Asegúrate de estar logueado en YouTube desde Edge/Chrome")
    print("2. Ejecuta: python server.py")
    print("3. Abre: http://localhost:5000")

if __name__ == "__main__":
    check_environment()
