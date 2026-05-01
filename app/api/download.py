"""Endpoints para descargas de video"""

from flask import Blueprint, request, jsonify, send_file
import os
from app.utils import downloader
import logging

logger = logging.getLogger(__name__)

download_bp = Blueprint('download', __name__, url_prefix='/api/download')

@download_bp.route('/audio', methods=['POST'])
def download_audio():
    """Endpoint para descargar audio (MP3)"""
    try:
        data = request.json
        url = data.get('url')
        quality = data.get('quality', '192')
        
        if not url:
            return jsonify({"error": "URL requerida"}), 400
        
        result = downloader.download_audio(url, quality)
        
        if result:
            return jsonify({
                "success": True,
                "message": "Audio descargado",
                "filename": result['filename'],
                "download_url": result['url'],
                "size": result['size']
            })
        else:
            return jsonify({"error": "Error al descargar audio"}), 500
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@download_bp.route('/video', methods=['POST'])
def download_video():
    """Endpoint para descargar video (MP4)"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL requerida"}), 400
        
        result = downloader.download_video(url)
        
        if result:
            return jsonify({
                "success": True,
                "message": "Video descargado",
                "filename": result['filename'],
                "download_url": result['url'],
                "size": result['size']
            })
        else:
            return jsonify({"error": "Error al descargar video"}), 500
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@download_bp.route('/<filename>', methods=['GET'])
def serve_file(filename):
    """Servir archivo descargado"""
    try:
        filepath = os.path.join(downloader.download_folder, filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "Archivo no encontrado"}), 404
        
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        logger.error(f"Error sirviendo archivo: {str(e)}")
        return jsonify({"error": str(e)}), 500
