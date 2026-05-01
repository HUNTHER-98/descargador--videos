"""Modelos de datos"""

class DownloadHistory:
    """Modelo para historial de descargas (preparado para BD futura)"""
    
    def __init__(self, url, platform, format_type, filename, size, timestamp=None):
        self.url = url
        self.platform = platform
        self.format_type = format_type
        self.filename = filename
        self.size = size
        self.timestamp = timestamp or __import__('datetime').datetime.now()
