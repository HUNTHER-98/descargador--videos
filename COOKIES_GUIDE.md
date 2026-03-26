Remove-Item cookies.txt -Force# Opción 1: Intentar con componentes remotos
yt-dlp --remote-components ejs:github https://www.youtube.com/watch?v=3alGZKwhlt0 -e 2>&1 | head -20# 🍪 Cómo Obtener Cookies para YouTube

Si ves el error `Failed to extract any player response`, necesitas cookies válidas de YouTube.

## ✅ Opción 1: Usar Netscape Cookie Editor (RECOMENDADO)

### Paso 1: Instalar la extensión
1. Abre **Microsoft Edge**
2. Ve a: `edge://extensions/`
3. Busca **"Netscape Cookie Editor"** o **"Cookie-Editor"**
4. Instala la extensión desde la tienda oficial

### Paso 2: Obtener cookies
1. Abre YouTube: https://www.youtube.com
2. Haz clic en la extensión de cookies
3. Haz clic en **"Export"** o **"Descargar"**
4. Se descargará un archivo `cookies.json` o similar

### Paso 3: Convertir a formato Netscape
1. Abre los cookies descargados con un editor de texto
2. Convierte a formato netscape si es necesario o...
3. Simplemente guarda como `cookies.txt` en la carpeta `descargador`

### Paso 4: Reinicia el servidor
```bash
python server.py
```

---

## ✅ Opción 2: Exportar desde chrome-cookies (Alternativa)

Si tienes Google Chrome:
1. Abre **Chrome**
2. Instala la extensión **"Get Cookies.txt LOCALLY"**
3. Ve a YouTube
4. Haz clic en la extensión y descarga los cookies
5. Guarda el archivo como `cookies.txt` en la carpeta `descargador`

---

## 📝 Formato esperado de cookies.txt

El archivo debe verse así:
```
# Netscape HTTP Cookie File
# This is a generated file!  Do not edit.

.youtube.com	TRUE	/	TRUE	1735689600	__Secure-1PSID	value...
.youtube.com	TRUE	/	TRUE	1735689600	__Secure-3PSID	value...
.youtube.com	TRUE	/	TRUE	1735689600	SAPISID	value...
```

---

## ⚠️ Si nada funciona

1. **Verifica que Edge/Chrome está actualizado**
2. **Cierra todas las ventanas de YouTube antes de exportar cookies**
3. **Los cookies expiran - exporta unos nuevos cada mes**
4. **Si el video es privado o restringido, no se puede descargar**

---

## 🔧 Diagnóstico

Para verificar que los cookies se cargan correctamente, mira los logs del servidor:

```
2026-02-20 12:34:56,789 - INFO - ✅ Usando archivo de cookies: cookies.txt
```

Si ves este mensaje, las cookies están siendo usadas.

---

**¡Prueba nuevamente después de agregar los cookies!** 🎉
