from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import yt_dlp
import os
import logging
import uuid
import re
import subprocess
import json
from datetime import datetime

app = Flask(__name__, template_folder='.')
CORS(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración
DOWNLOAD_FOLDER = 'downloads'
MAX_FILE_AGE_HOURS = 24  # Eliminar archivos después de 24 horas
COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'cookies.txt')

# Ruta a FFmpeg (instalado localmente)
FFMPEG_PATH = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-full_build', 'bin', 'ffmpeg.exe')
FFPROBE_PATH = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.0.1-full_build', 'bin', 'ffprobe.exe')

# Crear carpeta de descargas si no existe
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    """Limpia el nombre de archivo de caracteres inválidos"""
    # Remover caracteres no permitidos en nombres de archivo
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limitar longitud
    if len(filename) > 150:
        filename = filename[:150]
    return filename.strip()

def get_base_ydl_opts():
    """Obtiene opciones base para yt-dlp con soporte para componentes remotos"""
    
    # Carpeta para cachés de componentes
    home_dir = os.path.expanduser('~')
    ej_cache_dir = os.path.join(home_dir, '.cache', 'yt-dlp', 'ej')
    os.makedirs(ej_cache_dir, exist_ok=True)
    
    # Establecer variables de entorno para componentes
    os.environ['YT_DLP_EJ_DIR'] = ej_cache_dir
    
    opts = {
        'quiet': False,
        'no_warnings': True,
        'no_playlist': True,
        'socket_timeout': 90,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Ch-Ua': '"Chromium";v="131", "Microsoft Edge";v="131", "Not?A_Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
        },
        'sleep_interval': 1,
        'sleep_interval_requests': 1,
        'max_sleep_interval': 3,
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'web', 'android'],
                'skip': ['dash', 'hls', 'translated_subs'],
                'lang': ['en'],
            }
        },
        'retries': 50,
        'fragment_retries': 50,
        'skip_unavailable_fragments': True,
        'ffmpeg_location': FFMPEG_PATH,
        'allow_unplayable_formats': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
        'check_formats': False,
        'noprogress': True,
        'verbose': False,
        'no_check_certificate': True,
        'prefer_insecure': True,
        'proxy': '',
    }
    
    # Usar archivo de cookies si existe
    if os.path.exists(COOKIES_FILE):
        file_size = os.path.getsize(COOKIES_FILE)
        if file_size > 100:
            opts['cookiefile'] = COOKIES_FILE
            logging.info(f"✅ Usando archivo de cookies")
        else:
            logging.warning(f"⚠️  Archivo de cookies vacío")
    
    logging.info(f"✅ Componentes EJ cache: {ej_cache_dir}")
    return opts

def detect_platform(url):
    """Detecta la plataforma de la URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    elif 'instagram.com' in url or 'instagram.com/p/' in url:
        return 'instagram'
    else:
        return 'unknown'

def cleanup_old_files():
    """Eliminar archivos antiguos"""
    try:
        current_time = datetime.now()
        for filename in os.listdir(DOWNLOAD_FOLDER):
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                age_hours = (current_time - file_time).total_seconds() / 3600
                if age_hours > MAX_FILE_AGE_HOURS:
                    os.remove(filepath)
                    logging.info(f"Eliminado archivo antiguo: {filename}")
    except Exception as e:
        logging.error(f"Error limpiando archivos: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servidor está funcionando"""
    return jsonify({"status": "ok", "message": "Servidor funcionando"})

@app.route('/')
def index():
    """Servir el archivo HTML principal"""
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def get_video_info():
    """Obtener información del video usando componentes remotos"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL requerida"}), 400
        
        # Limpiar URL de parámetros de playlist
        if '&list=' in url:
            url = url.split('&list=')[0]
        
        # Usar subprocess para obtener información con componentes remotos
        cmd = [
            'yt-dlp',
            '--remote-components', 'ejs:github',
            '--dump-json',
            '--no-playlist',
            url
        ]
        
        logging.info(f"📊 Obteniendo información del video: {url}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            info = json.loads(result.stdout)
            
            return jsonify({
                "success": True,
                "title": info.get('title', 'Video'),
                "author": info.get('uploader', 'Desconocido'),
                "length": info.get('duration', 0),
                "views": info.get('view_count', 0),
                "thumbnail": info.get('thumbnail', ''),
                "qualities": ["720p", "480p", "360p"],
                "url": url
            })
        else:
            error_msg = result.stderr or result.stdout
            logging.error(f"Error obteniendo info: {error_msg}")
            return jsonify({"error": f"Error al obtener información: {error_msg[:200]}"}), 500
        
    except subprocess.TimeoutExpired:
        logging.error("Timeout al obtener información")
        return jsonify({"error": "Tiempo de espera excedido"}), 500
    except Exception as e:
        logging.error(f"Error obteniendo info: {str(e)}")
        return jsonify({"error": f"Error al obtener información: {str(e)}"}), 500

@app.route('/download', methods=['POST'])
def download_video():
    """Descargar video o audio usando subprocess con componentes remotos"""
    cleanup_old_files()
    
    try:
        data = request.json
        url = data.get('url')
        format_type = data.get('format', 'audio')
        
        if not url:
            return jsonify({"error": "URL requerida"}), 400
        
        # Limpiar URL de parámetros de playlist
        if '&list=' in url:
            url = url.split('&list=')[0]
        
        # Usar subprocess para llamar yt-dlp con componentes remotos
        # Esto fuerza a descargar los solucionadores de JavaScript de GitHub
        
        if format_type == 'audio':
            output_template = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
            cmd = [
                'yt-dlp',
                '--remote-components', 'ejs:github',  # Descargar componentes de GitHub
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', '192',
                '-o', output_template,
                '--no-playlist',
                '--socket-timeout', '90',
                url
            ]
            
            logging.info(f"🎵 Descargando audio (con componentes remotos): {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logging.info(f"✅ Audio descargado exitosamente")
                
                # Buscar el archivo descargado
                files = os.listdir(DOWNLOAD_FOLDER)
                for file in files:
                    if file.endswith('.mp3'):
                        filename = file
                        download_url = f'/download/{filename}'
                        file_size = os.path.getsize(os.path.join(DOWNLOAD_FOLDER, filename))
                        
                        return jsonify({
                            "success": True,
                            "message": "Descarga completada",
                            "title": os.path.splitext(filename)[0],
                            "format": "mp3",
                            "filename": filename,
                            "download_url": download_url,
                            "file_size": file_size
                        })
                
                return jsonify({
                    "success": True,
                    "message": "Descarga completada",
                    "format": "mp3",
                    "filename": "audio.mp3",
                    "download_url": "/download/audio.mp3",
                    "file_size": 0
                })
            else:
                error_msg = result.stderr or result.stdout
                logging.error(f"❌ Error descargando audio: {error_msg}")
                return jsonify({
                    "error": f"Error al descargar audio: {error_msg[:200]}"
                }), 500
        
        elif format_type == 'video':
            output_template = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
            cmd = [
                'yt-dlp',
                '--remote-components', 'ejs:github',
                '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                '-o', output_template,
                '--no-playlist',
                '--socket-timeout', '90',
                url
            ]
            
            logging.info(f"🎬 Descargando video (con componentes remotos): {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logging.info(f"✅ Video descargado exitosamente")
                
                # Buscar el archivo descargado
                files = os.listdir(DOWNLOAD_FOLDER)
                for file in files:
                    if file.endswith('.mp4'):
                        filename = file
                        download_url = f'/download/{filename}'
                        file_size = os.path.getsize(os.path.join(DOWNLOAD_FOLDER, filename))
                        
                        return jsonify({
                            "success": True,
                            "message": "Descarga completada",
                            "title": os.path.splitext(filename)[0],
                            "format": "mp4",
                            "filename": filename,
                            "download_url": download_url,
                            "file_size": file_size
                        })
                
                return jsonify({
                    "success": True,
                    "message": "Descarga completada",
                    "format": "mp4",
                    "filename": "video.mp4",
                    "download_url": "/download/video.mp4",
                    "file_size": 0
                })
            else:
                error_msg = result.stderr or result.stdout
                logging.error(f"❌ Error descargando video: {error_msg}")
                return jsonify({
                    "error": f"Error al descargar video: {error_msg[:200]}"
                }), 500
        else:
            return jsonify({"error": "Formato no soportado"}), 400
            
    except subprocess.TimeoutExpired:
        logging.error("❌ Timeout en la descarga (más de 10 minutos)")
        return jsonify({"error": "Tiempo de descarga excedido"}), 500
    except Exception as e:
        logging.error(f"Error en descarga: {str(e)}")
        return jsonify({"error": f"Error al descargar: {str(e)}"}), 500

@app.route('/download/<filename>', methods=['GET'])
def serve_file(filename):
    """Servir archivo descargado"""
    try:
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "Archivo no encontrado"}), 404
        
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        logging.error(f"Error sirviendo archivo: {str(e)}")
        return jsonify({"error": "Error al servir el archivo"}), 500

@app.route('/search', methods=['POST'])
def search_videos():
    """Buscar videos en YouTube"""
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({"error": "Término de búsqueda requerido"}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{10}:{query}", download=False)
            results = []
            
            for video in info['entries']:
                results.append({
                    "title": video.get('title', ''),
                    "author": video.get('uploader', ''),
                    "video_id": video.get('id', ''),
                    "thumbnail": video.get('thumbnail', ''),
                    "duration": video.get('duration', 0),
                    "url": video.get('webpage_url', '')
                })
            
            return jsonify({
                "success": True,
                "results": results,
                "count": len(results)
            })
        
    except Exception as e:
        logging.error(f"Error en búsqueda: {str(e)}")
        return jsonify({"error": f"Error en búsqueda: {str(e)}"}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🎵 SERVIDOR DE DESCARGAS DE YOUTUBE")
    print("=" * 50)
    print("\n⚠️  IMPORTANTE: Necesitas instalar las dependencias primero:")
    print("1. pip install flask pytube")
    print("2. pip install flask-cors")
    print("\n✅ Servidor iniciado en: http://localhost:5000")
    print("📁 Descargas se guardarán en: /downloads")
    print("\n🔧 Iniciando servidor...")
    
    app.run(host='0.0.0.0', port=5000, debug=True)