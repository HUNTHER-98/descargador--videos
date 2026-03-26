#!/usr/bin/env python3
"""
Script para obtener y guardar cookies de YouTube automáticamente
"""

import os
import sys
import http.cookiejar as cookiejar

def get_cookies_from_browser():
    """Obtiene cookies del navegador y las guarda en cookies.txt"""
    print("🍪 Extrayendo Cookies de YouTube")
    print("-" * 50)
    
    try:
        import browser_cookie3
        
        print("\n📱 Intentando obtener cookies de Edge...")
        try:
            edge_cookies = browser_cookie3.edge()
            youtube_cookies = [c for c in edge_cookies if 'youtube.com' in c.domain]
            
            if youtube_cookies:
                print(f"✅ Encontradas {len(youtube_cookies)} cookies de YouTube")
                save_cookies_to_file(youtube_cookies)
                return True
        except Exception as e:
            print(f"⚠️  Edge: {e}")
        
        print("\n📱 Intentando obtener cookies de Chrome...")
        try:
            chrome_cookies = browser_cookie3.chrome()
            youtube_cookies = [c for c in chrome_cookies if 'youtube.com' in c.domain]
            
            if youtube_cookies:
                print(f"✅ Encontradas {len(youtube_cookies)} cookies de YouTube")
                save_cookies_to_file(youtube_cookies)
                return True
        except Exception as e:
            print(f"⚠️  Chrome: {e}")
        
        print("\n📱 Intentando obtener cookies de Firefox...")
        try:
            firefox_cookies = browser_cookie3.firefox()
            youtube_cookies = [c for c in firefox_cookies if 'youtube.com' in c.domain]
            
            if youtube_cookies:
                print(f"✅ Encontradas {len(youtube_cookies)} cookies de YouTube")
                save_cookies_to_file(youtube_cookies)
                return True
        except Exception as e:
            print(f"⚠️  Firefox: {e}")
        
        print("\n❌ No se pudieron obtener cookies de ningún navegador")
        return False
        
    except ImportError:
        print("❌ browser-cookie3 no está instalado")
        print("\nInstala con: pip install browser-cookie3")
        return False

def save_cookies_to_file(cookies):
    """Guarda las cookies en formato Netscape"""
    filename = 'cookies.txt'
    
    try:
        with open(filename, 'w') as f:
            f.write("# Netscape HTTP Cookie File\n")
            f.write("# Cookies de YouTube - Generado automáticamente\n\n")
            
            for cookie in cookies:
                if hasattr(cookie, 'domain') and 'youtube' in cookie.domain:
                    # Formato: domain flag path secure expiry name value
                    expiry = int(cookie.expires) if hasattr(cookie, 'expires') and cookie.expires else 0
                    secure = "TRUE" if (hasattr(cookie, 'secure') and cookie.secure) else "FALSE"
                    
                    line = f"{cookie.domain}\tTRUE\t{cookie.path if hasattr(cookie, 'path') else '/'}\t{secure}\t{expiry}\t{cookie.name}\t{cookie.value}\n"
                    f.write(line)
        
        print(f"\n✅ Cookies guardadas en: {filename}")
        print("\nAhora:")
        print("1. Reinicia el servidor: python server.py")
        print("2. El servidor usará automáticamente estas cookies")
        return True
        
    except Exception as e:
        print(f"\n❌ Error guardando cookies: {e}")
        return False

def main():
    print("╔═══════════════════════════════════════════════════════╗")
    print("║          Extractor de Cookies de YouTube              ║")
    print("╚═══════════════════════════════════════════════════════╝\n")
    
    print("📋 Requisitos:")
    print("  1. Tener un navegador abierto con YouTube (Chrome, Edge o Firefox)")
    print("  2. Estar logueado en YouTube")
    print("  3. Haber navegado a youtube.com recientemente\n")
    
    if get_cookies_from_browser():
        print("\n" + "=" * 50)
        print("✅ ¡Éxito! Las cookies están listas para usar")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ No se pudieron obtener las cookies")
        print("=" * 50)
        print("\nTienes dos opciones:")
        print("\n1. Intenta de nuevo:")
        print("   - Abre tu navegador")
        print("   - Ve a YouTube y asegúrate de estar logueado")
        print("   - Ejecuta este script nuevamente")
        print("\n2. Crea manualmente cookies.txt:")
        print("   Ver README_SOLUCION.md para instrucciones")

if __name__ == "__main__":
    main()
