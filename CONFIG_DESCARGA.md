# Configuración de Carpetas de Descarga

## Resumen de Cambios

Se ha configurado la aplicación para separar automáticamente los archivos descargados en carpetas específicas según su tipo:

- **`downloads/audio/`** - Archivos de audio (MP3)
- **`downloads/video/`** - Archivos de video (MP4)

## Cambios Realizados

### 1. Estructura de Carpetas
```
downloads/
├── audio/     (Archivos MP3)
└── video/     (Archivos MP4)
```

### 2. Configuración en `server.py`

- ✅ Las descargas de **audio** se guardan en `downloads/audio/`
- ✅ Las descargas de **video** se guardan en `downloads/video/`
- ✅ Se asignan automáticamente permisos de lectura y escritura
- ✅ Las carpetas se crean automáticamente al iniciar la aplicación

### 3. Cambios en las Rutas de Descarga
- Audio: `/download/audio/{filename}`
- Video: `/download/video/{filename}`

## Uso

### Opción 1: Script Python (Multiplataforma)
```bash
python setup_permissions.py
```

Este script:
- Crea las carpetas si no existen
- Configura permisos correctos automáticamente
- Funciona en Windows, Linux y macOS

### Opción 2: Script PowerShell (Solo Windows)
```powershell
.\setup_permissions.ps1
```

Este script:
- Crea las carpetas si no existen
- Asigna permisos de modificación a "Everyone"
- Es más rápido en sistemas Windows

### Opción 3: Automático
El servidor `server.py` crea y configura automáticamente las carpetas al iniciar.

## Permisos Configurados

### En Windows
- Se asignan permisos "Modify" a "Everyone"
- Permite lectura y escritura para todos los usuarios

### En Unix/Linux/macOS
- Permisos: `rwxrwxrwx` (755)
- Lectura, escritura y ejecución para propietario, grupo y otros

## Funcionamiento

### Descarga de Audio
1. Usuario solicita descarga de audio
2. El archivo se descarga en `downloads/audio/`
3. Se asignan permisos automáticamente
4. La URL devuelta es: `/download/audio/{nombre_archivo}.mp3`

### Descarga de Video
1. Usuario solicita descarga de video
2. El archivo se descarga en `downloads/video/`
3. Se asignan permisos automáticamente
4. La URL devuelta es: `/download/video/{nombre_archivo}.mp4`

## Limpieza Automática

Los archivos más antiguos de 24 horas se eliminan automáticamente de ambas carpetas:
- Limpieza de `downloads/audio/` - archivos > 24 horas
- Limpieza de `downloads/video/` - archivos > 24 horas

## Verificación

Para verificar que los permisos están correctamente configurados:

### En Windows (cmd/PowerShell)
```powershell
icacls downloads\audio
icacls downloads\video
```

### En Unix/Linux/macOS
```bash
ls -la downloads/
ls -la downloads/audio/
ls -la downloads/video/
```

## Troubleshooting

Si encuentras problemas con permisos:

1. **En Windows (como Administrador):**
   ```powershell
   .\setup_permissions.ps1
   ```

2. **En Unix/Linux (con sudo si es necesario):**
   ```bash
   python setup_permissions.py
   ```

3. **Manual:**
   ```bash
   # Linux/macOS
   chmod -R 777 downloads/
   
   # Windows (en cmd como administrador)
   icacls "downloads" /grant:r Everyone:F /T /C /Q
   ```

## Archivo de Configuración

Los siguientes archivos han sido creados/modificados:

- ✅ `server.py` - Lógica de descarga actualizada
- ✅ `setup_permissions.py` - Script de configuración Python
- ✅ `setup_permissions.ps1` - Script de configuración PowerShell
- ℹ️ `CONFIG_DESCARGA.md` - Este archivo

