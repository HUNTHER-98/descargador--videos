"""Utilidades para descargar videos de múltiples plataformas"""

import subprocess
import os
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class VideoDownloader:
    """Descargador universal de videos"""
    
    def __init__(self, ffmpeg_path=None):
        self.ffmpeg_path = ffmpeg_path
        self.download_folder = 'downloads'
        os.makedirs(self.download_folder, exist_ok=True)
    
    def get_video_info(self, url, platform='youtube'):
        """Obtiene información del video usando yt-dlp"""
        try:
            cmd = [
                'yt-dlp',
                '--remote-components', 'ejs:github',
                '--dump-json',
                '--no-playlist',
                url
            ]
            
            logger.info(f"📊 Obteniendo información de {platform}: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                logger.error(f"Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout al obtener información")
            return None
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return None
    
    def search_videos(self, query, platform='youtube', limit=5):
        """Busca videos en una plataforma"""
        try:
            cmd = [
                'yt-dlp',
                '-j',
                f'ytsearch{limit}:{query}' if platform == 'youtube' else query,
                '--socket-timeout', '90'
            ]
            
            logger.info(f"🔍 Buscando en {platform}: {query}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                videos = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            videos.append(json.loads(line))
                        except:
                            pass
                return videos
            else:
                logger.error(f"Error en búsqueda: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout en búsqueda")
            return []
        except Exception as e:
            logger.error(f"Error en búsqueda: {str(e)}")
            return []
    
    def download_audio(self, url, quality='192'):
        """Descargar audio en MP3"""
        try:
            output_template = os.path.join(self.download_folder, '%(title)s.%(ext)s')
            cmd = [
                'yt-dlp',
                '--remote-components', 'ejs:github',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', quality,
                '-o', output_template,
                '--no-playlist',
                '--socket-timeout', '90',
                url
            ]
            
            logger.info(f"🎵 Descargando audio: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("✅ Audio descargado exitosamente")
                return self._find_latest_file('.mp3')
            else:
                logger.error(f"Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout en descarga")
            return None
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return None
    
    def download_video(self, url, format_type='mp4'):
        """Descargar video en MP4 o WebM"""
        try:
            output_template = os.path.join(self.download_folder, '%(title)s.%(ext)s')
            cmd = [
                'yt-dlp',
                '--remote-components', 'ejs:github',
                '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                '-o', output_template,
                '--no-playlist',
                '--socket-timeout', '90',
                url
            ]
            
            logger.info(f"🎬 Descargando video: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info("✅ Video descargado exitosamente")
                return self._find_latest_file(('.mp4', '.webm'))
            else:
                logger.error(f"Error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout en descarga")
            return None
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return None
    
    def _find_latest_file(self, extensions):
        """Encuentra el archivo más reciente descargado"""
        try:
            if isinstance(extensions, str):
                extensions = [extensions]
            
            files = []
            for filename in os.listdir(self.download_folder):
                if any(filename.endswith(ext) for ext in extensions):
                    filepath = os.path.join(self.download_folder, filename)
                    files.append((filepath, os.path.getctime(filepath)))
            
            if not files:
                return None
            
            latest_file = sorted(files, key=lambda x: x[1])[-1][0]
            return {
                'filename': os.path.basename(latest_file),
                'path': latest_file,
                'size': os.path.getsize(latest_file),
                'url': f'/download/{os.path.basename(latest_file)}'
            }
        except Exception as e:
            logger.error(f"Error encontrando archivo: {str(e)}")
            return None

# Instancia global
downloader = VideoDownloader()
