#!/usr/bin/env python3
"""
Script de diagnóstico para probar descarga de YouTube sin cookies
"""

import yt_dlp
import os
import sys

# Ajustar encoding para Windows
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-full_build', 'bin', 'ffmpeg.exe')

def test_info_extraction(url):
    """Prueba obtener información del video"""
    print("\n[INFO] Prueba 1: Obtener información\n")
    
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'allow_unplayable_formats': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"[OK] Titulo: {info.get('title')}")
            print(f"[OK] Duracion: {info.get('duration')} seg")
            print(f"[OK] ID: {info.get('id')}")
            return True
    except Exception as e:
        print(f"[ERROR] {str(e)[:200]}")
        return False

def test_formats(url):
    """Prueba ver qué formatos están disponibles"""
    print("\n[INFO] Prueba 2: Formatos disponibles\n")
    
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'allformats': True,
        'allow_unplayable_formats': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            print(f"Total de formatos: {len(formats)}\n")
            
            for fmt in formats[:5]:
                print(f"  ID: {fmt.get('format_id'):<5} | " +
                      f"Codec: {fmt.get('vcodec', 'audio'):<10} | " +
                      f"Tamanio: {fmt.get('filesize', 'unknown')}")
            
            if len(formats) > 5:
                print(f"  ... y {len(formats) - 5} formatos mas")
            
            return len(formats) > 0
    except Exception as e:
        print(f"[ERROR] {str(e)[:200]}")
        return False

def test_download(url):
    """Prueba descargar audio"""
    print("\n[INFO] Prueba 3: Descargar audio en MP3\n")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'test_download.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'ffmpeg_location': FFMPEG_PATH,
        'socket_timeout': 30,
        'retries': 5,
        'fragment_retries': 5,
        'allow_unplayable_formats': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            mp3_file = 'test_download.mp3'
            if os.path.exists(mp3_file):
                size_kb = os.path.getsize(mp3_file) / 1024
                print(f"[OK] Archivo descargado: {mp3_file}")
                print(f"[OK] Tamanio: {size_kb:.1f} KB")
                os.remove(mp3_file)
                return True
            else:
                print(f"[ERROR] No se creo el archivo MP3")
                return False
                
    except Exception as e:
        print(f"[ERROR] {str(e)[:300]}")
        return False

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    print("="*60)
    print("[DIAGNOSTICO] DE DESCARGA DE YOUTUBE")
    print("="*60)
    print(f"\nURL: {url}")
    print(f"FFmpeg: {FFMPEG_PATH}")
    print(f"Existe: {os.path.exists(FFMPEG_PATH)}")
    
    results = []
    results.append(("Obtener informacion", test_info_extraction(url)))
    results.append(("Ver formatos", test_formats(url)))
    results.append(("Descargar audio", test_download(url)))
    
    print("\n" + "="*60)
    print("[RESUMEN]")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[OK]" if result else "[FALLO]"
        print(f"{name:<30} {status}")
    
    print(f"\nResultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n[OK] Todo funciona correctamente!")
    elif passed > 0:
        print("\n[ADVERTENCIA] Algunas pruebas fallaron. Intenta agregar cookies.txt")
    else:
        print("\n[ERROR] Ninguna prueba funciono. Necesitas cookies validos de YouTube")
    
    print("\n[INFO] Para obtener cookies: lee COOKIES_GUIDE.md")
    print("="*60)
