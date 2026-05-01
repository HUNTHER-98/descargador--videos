"""Endpoints para información y búsqueda de videos"""

from flask import Blueprint, request, jsonify
from app.utils import downloader
import logging

logger = logging.getLogger(__name__)

info_bp = Blueprint('info', __name__, url_prefix='/api/info')

@info_bp.route('/video', methods=['POST'])
def get_video_info():
    """Obtener información del video"""
    try:
        data = request.json
        url = data.get('url')
        platform = data.get('platform', 'youtube')
        
        if not url:
            return jsonify({"error": "URL requerida"}), 400
        
        info = downloader.get_video_info(url, platform)
        
        if info:
            return jsonify({
                "success": True,
                "title": info.get('title', 'Video'),
                "author": info.get('uploader', 'Desconocido'),
                "duration": info.get('duration', 0),
                "views": info.get('view_count', 0),
                "thumbnail": info.get('thumbnail', ''),
                "url": url
            })
        else:
            return jsonify({"error": "Error al obtener información"}), 500
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@info_bp.route('/search', methods=['POST'])
def search_videos():
    """Buscar videos en una plataforma"""
    try:
        data = request.json
        query = data.get('query')
        platform = data.get('platform', 'youtube')
        limit = data.get('limit', 5)
        
        if not query:
            return jsonify({"error": "Búsqueda requerida"}), 400
        
        videos = downloader.search_videos(query, platform, limit)
        
        # Procesar resultados
        results = []
        for v in videos:
            results.append({
                'title': v.get('title', 'Video'),
                'id': v.get('id', ''),
                'url': v.get('url', ''),
                'duration': v.get('duration', 0),
                'uploader': v.get('uploader', 'Desconocido'),
                'thumbnail': v.get('thumbnail', ''),
                'views': v.get('view_count', 0)
            })
        
        return jsonify({
            "success": True,
            "platform": platform,
            "query": query,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}")
        return jsonify({"error": str(e)}), 500
