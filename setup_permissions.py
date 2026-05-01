#!/usr/bin/env python3
"""
Script para configurar permisos correctos en las carpetas de descarga
Uso: python setup_permissions.py
"""

import os
import stat
import sys

def setup_permissions():
    """Configura permisos de lectura y escritura en carpetas de descarga"""
    
    folders = [
        'downloads',
        'downloads/audio',
        'downloads/video'
    ]
    
    print("🔧 Configurando permisos de carpetas de descarga...\n")
    
    for folder in folders:
        try:
            # Crear carpeta si no existe
            os.makedirs(folder, exist_ok=True)
            
            # Configurar permisos: lectura y escritura para todos
            # En Windows: FILE_GENERIC_READ | FILE_GENERIC_WRITE
            # En Unix: rwxrwxrwx
            if sys.platform == 'win32':
                # Para Windows
                os.system(f'icacls "{folder}" /grant:r Everyone:F /T /C /Q')
                print(f"✅ Permisos configurados para: {folder}")
            else:
                # Para Unix/Linux/macOS
                os.chmod(folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                print(f"✅ Permisos configurados para: {folder}")
                
        except Exception as e:
            print(f"❌ Error en {folder}: {e}")
            return False
    
    print("\n✅ Permisos configurados exitosamente!")
    return True

if __name__ == '__main__':
    setup_permissions()
