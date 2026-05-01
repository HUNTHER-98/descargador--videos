"""Configuración de la aplicación"""

import os

class Config:
    """Configuración base"""
    
    # Servidor
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Descargas
    DOWNLOAD_FOLDER = 'downloads'
    MAX_FILE_AGE_HOURS = 24
    
    # Plataformas soportadas
    SUPPORTED_PLATFORMS = [
        'youtube',  # ✅ Funciona
        'tiktok',   # ✅ Funciona
        'instagram', # 🔜 Próximamente
        'facebook',  # 🔜 Próximamente
        'vimeo'      # 🔜 Próximamente
    ]
    
    # Calidades disponibles
    AUDIO_QUALITIES = ['128', '192', '256', '320']
    VIDEO_FORMATS = ['mp4', 'webm']
    
    # Paths
    FFMPEG_PATH = os.path.join(os.path.dirname(__file__), '..', 'ffmpeg-8.0.1-full_build', 'bin', 'ffmpeg.exe')
    FFPROBE_PATH = os.path.join(os.path.dirname(__file__), '..', 'ffmpeg-8.0.1-full_build', 'bin', 'ffprobe.exe')


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DOWNLOAD_FOLDER = 'test_downloads'


# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
