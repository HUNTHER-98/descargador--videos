#!/usr/bin/env python3
"""
Script para extraer cookies de Edge y guardarlas en formato netscape
"""

import sys
import os

try:
    import browser_cookie3
    print("✅ browser_cookie3 importado correctamente")
except ImportError:
    print("❌ browser_cookie3 no está instalado")
    print("Instalando...")
    os.system("pip install browser-cookie3")
    import browser_cookie3

print("\n📱 Extrayendo cookies de Edge...\n")

try:
    # Obtener cookies de Edge
    cj = browser_cookie3.edge()
    print(f"✅ Se encontraron {len(cj)} cookies\n")
    
    # Guardar en formato netscape (compatible con yt-dlp)
    output_file = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    
    with open(output_file, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This is a generated file!  Do not edit.\n\n")
        
        for cookie in cj:
            # Formato netscape: domain flag path secure expiration name value
            secure = "TRUE" if cookie.secure else "FALSE"
            expires = int(cookie.expires) if cookie.expires else "0"
            domain = cookie.domain
            path = cookie.path or "/"
            
            line = f"{domain}\tTRUE\t{path}\t{secure}\t{expires}\t{cookie.name}\t{cookie.value}\n"
            f.write(line)
    
    print(f"✅ Cookies guardadas en: {output_file}")
    print(f"📝 Total de cookies: {len(cj)}")
    
except Exception as e:
    print(f"❌ Error extrayendo cookies: {str(e)}")
    print("\n💡 Solución alternativa:")
    print("   1. Abre Edge")
    print("   2. Ve a https://www.youtube.com")
    print("   3. Haz login en tu cuenta de Google")
    print("   4. El script intentará usar nuevamente")
    sys.exit(1)

print("\n✅ ¡Cookies extraídas exitosamente!")
print("🚀 Ahora reinicia el servidor (server.py) para usar las cookies")
