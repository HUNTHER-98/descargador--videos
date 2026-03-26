#!/usr/bin/env python3
"""
Script de instalación y verificación del descargador
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print('='*60)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Error en: {description}")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🚀 INSTALADOR DEL DESCARGADOR DE VIDEO Y AUDIO")
    print("="*60)
    
    # Verificar Python
    print(f"\n✅ Python versión: {sys.version}")
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias...")
    
    dependencies = [
        ("pip install --upgrade pip", "Actualizar pip"),
        ("pip install -r requirements.txt", "Instalar paquetes de requirements.txt"),
    ]
    
    all_success = True
    for cmd, desc in dependencies:
        if not run_command(cmd, desc):
            all_success = False
    
    # Verificar FFmpeg
    print(f"\n{'='*60}")
    print("🎬 Verificando FFmpeg")
    print('='*60)
    
    result = subprocess.run("ffmpeg -version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ FFmpeg está instalado")
        lines = result.stdout.split('\n')[:1]
        print(lines[0])
    else:
        print("⚠️  FFmpeg no está instalado")
        print("\n📥 Por favor instala FFmpeg:")
        print("   Windows (con Chocolatey): choco install ffmpeg")
        print("   Windows (manual): Descárgalo de https://ffmpeg.org/download.html")
        print("   Linux (Ubuntu): sudo apt-get install ffmpeg")
        print("   macOS: brew install ffmpeg")
        print("\n❌ Sin FFmpeg no podrás descargar MP3 desde YouTube")
        all_success = False
    
    # Resumen
    print(f"\n{'='*60}")
    if all_success:
        print("✅ INSTALACIÓN COMPLETADA")
        print("\n🚀 Para iniciar el servidor ejecuta:")
        print("   python server.py")
        print("\n📂 Luego abre index.html en tu navegador")
    else:
        print("⚠️  INSTALACIÓN PARCIALMENTE COMPLETADA")
        print("   Por favor, revisa los errores arriba")
    
    print('='*60 + "\n")

if __name__ == '__main__':
    main()
