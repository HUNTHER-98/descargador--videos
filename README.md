# 📥 Descargador de Videos - YouTube & Más

Descargador web moderno para descargar audio y video de YouTube con interfaz amigable. Soporta descarga en MP3 y MP4 con componentes remotos para eludir protecciones de YouTube.

## ✨ Características

- ✅ **Descarga de YouTube** - Audio (MP3) y Video (MP4)
- ✅ **Interfaz Web** - Intuitiva y responsive
- ✅ **Componentes Remotos** - Resuelve desafíos JavaScript de YouTube automáticamente
- ✅ **Sin Bloqueos** - Usando `--remote-components ejs:github`
- ✅ **Multiplataforma** - Windows, Linux, macOS, Termux
- 🚀 **API REST** - Endpoints para integración

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8+
- FFmpeg
- pip

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/descargador-videos.git
cd descargador-videos
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar el servidor

```bash
python server.py
```

Luego accede a: **http://localhost:5000**

## 📱 Uso en Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install -y python python-dev clang ffmpeg
git clone https://github.com/TU_USUARIO/descargador-videos.git
cd descargador-videos
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

## 🎯 Endpoints API

### GET `/health`
Verifica si el servidor está activo.

### POST `/info`
Obtiene información del video.

**Body:**
```json
{"url": "https://www.youtube.com/watch?v=..."}
```

### POST `/download`
Descarga audio o video.

**Body:**
```json
{"url": "https://www.youtube.com/watch?v=...", "format": "audio"}
```

**Parámetros:**
- `url`: URL del video
- `format`: `"audio"` (MP3) o `"video"` (MP4)

## ⚙️ Configuración

Modificar en `server.py`:
```python
DOWNLOAD_FOLDER = 'downloads'
MAX_FILE_AGE_HOURS = 24
```

## 🛠️ Solución de Problemas

### Error: "Failed to extract any player response"
```bash
pip install --upgrade yt-dlp
```

### Error: "ffmpeg not found"
- **Windows:** Descarga desde https://ffmpeg.org/download.html
- **Linux:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`

## 📋 Requisitos

```
Flask==2.3.3
yt-dlp>=2025.01.18
flask-cors==4.0.0
browser-cookie3>=0.6.4
```

## 🌐 Acceso desde otros dispositivos

Encuentra tu IP local y accede desde otro dispositivo:
```
http://TU_IP:5000
```

## 📝 Licencia

MIT License

## ⚠️ Aviso Legal

Uso personal y educativo solo. Respeta los derechos de autor.

---

**¡Disfruta descargando! 🎉**
