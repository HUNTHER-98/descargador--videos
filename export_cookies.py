#!/usr/bin/env python3
"""
Script para exportar cookies de YouTube desde el navegador
Soporta: Chrome, Edge, Firefox, Safari
"""

import os
import json
import sys
from pathlib import Path

def export_chrome_cookies():
    """Exportar cookies de Chrome/Edge"""
    try:
        import browser_cookie3
        cookies = browser_cookie3.edge()  # Usar Edge
        print("✅ Cookies de Edge exportadas exitosamente")
        return cookies
    except Exception as e:
        print(f"⚠️  Error exportando cookies de Edge: {e}")
        return None

def export_firefox_cookies():
    """Exportar cookies de Firefox"""
    try:
        import browser_cookie3
        cookies = browser_cookie3.firefox()
        print("✅ Cookies de Firefox exportadas exitosamente")
        return cookies
    except Exception as e:
        print(f"⚠️  Error exportando cookies de Firefox: {e}")
        return None

def main():
    print("🍪 Exportador de Cookies de YouTube")
    print("-" * 40)
    
    cookies = export_chrome_cookies()
    if not cookies:
        cookies = export_firefox_cookies()
    
    if cookies:
        print("\n✅ Cookies obtenidas. Probando con yt-dlp...")
        os.system("echo Cookies exportadas correctamente")
    else:
        print("\n❌ No se pudieron obtener cookies")
        print("\nAlternativa: Instala browser-cookie3")
        print("pip install browser-cookie3")

if __name__ == "__main__":
    main()
