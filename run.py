"""Punto de entrada principal de la aplicación - Versión 2.0 (escalada)"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from app.config import config
from app.api.download import download_bp
from app.api.info import info_bp

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Crear aplicación
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=TEMPLATES_DIR, static_url_path='')
CORS(app)

# Cargar configuración
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Registrar blueprints
app.register_blueprint(download_bp)
app.register_blueprint(info_bp)

# Crear carpeta de descargas
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_files(filename):
    """Servir archivos estáticos desde templates"""
    try:
        return send_from_directory(TEMPLATES_DIR, filename)
    except:
        return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "OK",
        "version": "2.0.0",
        "platforms": app.config['SUPPORTED_PLATFORMS']
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Obtener configuración disponible"""
    return jsonify({
        "platforms": app.config['SUPPORTED_PLATFORMS'],
        "audio_qualities": app.config['AUDIO_QUALITIES'],
        "video_formats": app.config['VIDEO_FORMATS']
    })

def show_startup_message():
    """Mostrar mensaje de inicio"""
    print("\n")
    print("=" * 60)
    print("✅ DESCARGADOR DE VIDEOS - VERSIÓN 2.0 (ESCALADA)")
    print("=" * 60)
    print(f"🌐 Servidor iniciado en: http://localhost:{app.config['PORT']}")
    print(f"📁 Descargas se guardarán en: {app.config['DOWNLOAD_FOLDER']}")
    print(f"🔧 Modo: {env.upper()}")
    print(f"📱 Plataformas: {', '.join(app.config['SUPPORTED_PLATFORMS'])}")
    print("=" * 60)
    print("\n")

if __name__ == '__main__':
    show_startup_message()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
