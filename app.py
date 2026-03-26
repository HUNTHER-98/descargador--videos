# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import yt_dlp
# import os
# import uuid
# import threading

# app = Flask(__name__)
# CORS(app)  # Esto permitirá peticiones desde el frontend

# # Configuración de yt-dlp
# ydl_opts = {
#     'quiet': True,
#     'no_warnings': True,
#     'outtmpl': 'downloads/%(title)s.%(ext)s',
# }

# # Crear la carpeta de descargas si no existe
# if not os.path.exists('downloads'):
#     os.makedirs('downloads')

# def cleanup_file(filepath, delay=300):
#     """Elimina el archivo después de un tiempo determinado (en segundos)"""
#     def remove_file():
#         import time
#         time.sleep(delay)
#         try:
#             if os.path.exists(filepath):
#                 os.remove(filepath)
#         except Exception as e:
#             print(f"Error al eliminar el archivo {filepath}: {e}")
#     threading.Thread(target=remove_file).start()

# @app.route('/download', methods=['POST'])
# def download():
#     data = request.get_json()
#     url = data.get('url')
#     format = data.get('format', 'mp3')

#     if not url:
#         return jsonify({'success': False, 'message': 'URL no proporcionada'}), 400

#     try:
#         # Configuración según el formato
#         if format == 'mp3':
#             ydl_opts['format'] = 'bestaudio/best'
#             ydl_opts['postprocessors'] = [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }]
#         elif format == 'mp4':
#             ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
#             ydl_opts['merge_output_format'] = 'mp4'
#         else:
#             return jsonify({'success': False, 'message': 'Formato no soportado'}), 400

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             # Obtener información del video
#             info = ydl.extract_info(url, download=False)
#             title = info.get('title', 'video')
            
#             # Descargar el video/audio
#             ydl.download([url])
            
#             # Encontrar el archivo descargado
#             filename = ydl.prepare_filename(info)
#             if format == 'mp3':
#                 filename = filename.rsplit('.', 1)[0] + '.mp3'
            
#             # Generar un nombre único para el archivo
#             unique_filename = f"{uuid.uuid4()}.{format}"
#             new_filepath = os.path.join('downloads', unique_filename)
#             os.rename(filename, new_filepath)

#             # Programar la eliminación del archivo después de 5 minutos
#             cleanup_file(new_filepath, 300)

#             # Devolver la URL de descarga
#             download_url = f"http://localhost:5000/download_file/{unique_filename}"
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Descarga completada',
#                 'title': title,
#                 'download_url': download_url
#             })

#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# @app.route('/download_file/<filename>')
# def download_file(filename):
#     filepath = os.path.join('downloads', filename)
#     if os.path.exists(filepath):
#         return send_file(filepath, as_attachment=True)
#     else:
#         return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


# ================================================================================


# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import yt_dlp
# import os
# import uuid
# import threading

# app = Flask(__name__)
# CORS(app)  # Esto permitirá peticiones desde el frontend

# # Configuración de yt-dlp
# ydl_opts = {
#     'quiet': True,
#     'no_warnings': True,
#     'outtmpl': 'downloads/%(title)s.%(ext)s',
#     'ffmpeg_location': r'C:\Users\LENOVO\Documents\descargador\ffmpeg-8.0.1\bin',  # Agregado
# }

# # Crear la carpeta de descargas si no existe
# if not os.path.exists('downloads'):
#     os.makedirs('downloads')

# def cleanup_file(filepath, delay=300):
#     """Elimina el archivo después de un tiempo determinado (en segundos)"""
#     def remove_file():
#         import time
#         time.sleep(delay)
#         try:
#             if os.path.exists(filepath):
#                 os.remove(filepath)
#         except Exception as e:
#             print(f"Error al eliminar el archivo {filepath}: {e}")
#     threading.Thread(target=remove_file).start()

# @app.route('/download', methods=['POST'])
# def download():
#     data = request.get_json()
#     url = data.get('url')
#     format = data.get('format', 'mp3')

#     if not url:
#         return jsonify({'success': False, 'message': 'URL no proporcionada'}), 400

#     try:
#         # Crear una copia de ydl_opts para esta descarga
#         current_opts = ydl_opts.copy()
        
#         # Configuración según el formato
#         if format == 'mp3':
#             current_opts['format'] = 'bestaudio/best'
#             current_opts['postprocessors'] = [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }]

#         elif format == 'mp4':
#             current_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
#             current_opts['merge_output_format'] = 'mp4'
#         else:
#             return jsonify({'success': False, 'message': 'Formato no soportado'}), 400

#         with yt_dlp.YoutubeDL(current_opts) as ydl:
#             # Obtener información del video
#             info = ydl.extract_info(url, download=False)
#             title = info.get('title', 'video')
            
#             # Descargar el video/audio
#             ydl.download([url])
            
#             # Encontrar el archivo descargado
#             filename = ydl.prepare_filename(info)
#             if format == 'mp3':
#                 filename = filename.rsplit('.', 1)[0] + '.mp3'
            
#             # Generar un nombre único para el archivo
#             unique_filename = f"{uuid.uuid4()}.{format}"
#             new_filepath = os.path.join('downloads', unique_filename)
#             os.rename(filename, new_filepath)

#             # Programar la eliminación del archivo después de 5 minutos
#             cleanup_file(new_filepath, 300)

#             # Devolver la URL de descarga
#             download_url = f"http://localhost:5000/download_file/{unique_filename}"
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Descarga completada',
#                 'title': title,
#                 'download_url': download_url
#             })

#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# @app.route('/download_file/<filename>')
# def download_file(filename):
#     filepath = os.path.join('downloads', filename)
#     if os.path.exists(filepath):
#         return send_file(filepath, as_attachment=True)
#     else:
#         return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
# ---------------------------------------------------------------------------------------
# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import yt_dlp
# import os
# import uuid
# import threading

# app = Flask(__name__)
# CORS(app)  # Esto permitirá peticiones desde el frontend

# # Crear la carpeta de descargas si no existe
# if not os.path.exists('downloads'):
#     os.makedirs('downloads')

# def cleanup_file(filepath, delay=300):
#     """Elimina el archivo después de un tiempo determinado (en segundos)"""
#     def remove_file():
#         import time
#         time.sleep(delay)
#         try:
#             if os.path.exists(filepath):
#                 os.remove(filepath)
#         except Exception as e:
#             print(f"Error al eliminar el archivo {filepath}: {e}")
#     threading.Thread(target=remove_file).start()

# @app.route('/download', methods=['POST'])
# def download():
#     data = request.get_json()
#     url = data.get('url')
#     format = data.get('format', 'mp3')

#     if not url:
#         return jsonify({'success': False, 'message': 'URL no proporcionada'}), 400

#     try:
#         # Configuración base
#         ydl_opts = {
#             'quiet': True,
#             'no_warnings': True,
#             'outtmpl': 'downloads/%(title)s.%(ext)s',
#             'ffmpeg_location': r'C:\Users\LENOVO\Documents\descargador\ffmpeg-8.0.1\bin',
#         }
        
#         # Configuración según el formato
#         if format == 'mp3':
#             ydl_opts['format'] = 'bestaudio/best'
#             ydl_opts['postprocessors'] = [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }]
#             ydl_opts['prefer_ffmpeg'] = True
            
#         elif format == 'mp4':
#             ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
#             ydl_opts['merge_output_format'] = 'mp4'
#             ydl_opts['postprocessors'] = [{
#                 'key': 'FFmpegVideoConvertor',
#                 'preferedformat': 'mp4',
#             }]
            
#         else:
#             return jsonify({'success': False, 'message': 'Formato no soportado'}), 400

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             # Obtener información del video
#             info = ydl.extract_info(url, download=False)
#             title = info.get('title', 'video')
            
#             # Descargar el video/audio
#             ydl.download([url])
            
#             # Encontrar el archivo descargado
#             filename = ydl.prepare_filename(info)
            
#             # Ajustar la extensión según el formato
#             if format == 'mp3':
#                 # Para MP3, cambiar la extensión
#                 base_filename = os.path.splitext(filename)[0]
#                 filename = base_filename + '.mp3'
#             elif format == 'mp4':
#                 # Para MP4, asegurarse de que tenga la extensión correcta
#                 base_filename = os.path.splitext(filename)[0]
#                 filename = base_filename + '.mp4'
            
#             # Generar un nombre único para el archivo
#             unique_filename = f"{uuid.uuid4()}.{format}"
#             new_filepath = os.path.join('downloads', unique_filename)
            
#             # Verificar que el archivo existe antes de renombrar
#             if os.path.exists(filename):
#                 os.rename(filename, new_filepath)
#             else:
#                 return jsonify({'success': False, 'message': f'Archivo no encontrado: {filename}'}), 500

#             # Programar la eliminación del archivo después de 5 minutos
#             cleanup_file(new_filepath, 300)

#             # Devolver la URL de descarga
#             download_url = f"http://localhost:5000/download_file/{unique_filename}"
            
#             return jsonify({
#                 'success': True,
#                 'message': 'Descarga completada',
#                 'title': title,
#                 'download_url': download_url
#             })

#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# @app.route('/download_file/<filename>')
# def download_file(filename):
#     filepath = os.path.join('downloads', filename)
#     if os.path.exists(filepath):
#         return send_file(filepath, as_attachment=True)
#     else:
#         return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
# ==============================================================================
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid
import threading

app = Flask(__name__)
CORS(app)  # Esto permitirá peticiones desde el frontend

# Crear la carpeta de descargas si no existe
if not os.path.exists('downloads'):
    os.makedirs('downloads')

def cleanup_file(filepath, delay=300):
    """Elimina el archivo después de un tiempo determinado (en segundos)"""
    def remove_file():
        import time
        time.sleep(delay)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error al eliminar el archivo {filepath}: {e}")
    threading.Thread(target=remove_file).start()

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    format = data.get('format', 'mp3')

    if not url:
        return jsonify({'success': False, 'message': 'URL no proporcionada'}), 400

    try:
        # Generar un nombre único para esta descarga
        unique_id = str(uuid.uuid4())
        
        # Configuración base
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'outtmpl': f'downloads/{unique_id}.%(ext)s',  # Nombre único temporal
            'ffmpeg_location': r'C:\Users\LENOVO\Documents\descargador\ffmpeg-8.0.1\bin',
        }
        
        # Configuración según el formato
        if format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            ydl_opts['keepvideo'] = False
            ydl_opts['writethumbnail'] = False
            
        elif format == 'mp4':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            ydl_opts['merge_output_format'] = 'mp4'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
            
        else:
            return jsonify({'success': False, 'message': 'Formato no soportado'}), 400

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obtener información del video
            print(f"Obteniendo información de: {url}")
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            
            # Descargar y procesar
            print(f"Descargando y procesando a {format}...")
            ydl.download([url])
            
            # El archivo procesado debería estar aquí
            processed_file = f'downloads/{unique_id}.{format}'
            
            print(f"Buscando archivo: {processed_file}")
            print(f"Archivos en downloads: {os.listdir('downloads')}")
            
            # Verificar que el archivo existe
            if os.path.exists(processed_file):
                print(f"✓ Archivo encontrado: {processed_file}")
                
                # Programar la eliminación del archivo después de 5 minutos
                cleanup_file(processed_file, 300)
                
                # Devolver la URL de descarga
                download_url = f"http://localhost:5000/download_file/{unique_id}.{format}"
                
                return jsonify({
                    'success': True,
                    'message': 'Descarga completada',
                    'title': title,
                    'download_url': download_url
                })
            else:
                # Listar todos los archivos para debug
                all_files = os.listdir('downloads')
                print(f"✗ Archivo no encontrado. Archivos disponibles: {all_files}")
                
                # Buscar cualquier archivo que empiece con el unique_id
                matching_files = [f for f in all_files if f.startswith(unique_id)]
                if matching_files:
                    actual_file = matching_files[0]
                    print(f"Archivo encontrado con nombre diferente: {actual_file}")
                    
                    # Renombrar al formato correcto
                    old_path = f'downloads/{actual_file}'
                    new_path = f'downloads/{unique_id}.{format}'
                    os.rename(old_path, new_path)
                    
                    cleanup_file(new_path, 300)
                    download_url = f"http://localhost:5000/download_file/{unique_id}.{format}"
                    
                    return jsonify({
                        'success': True,
                        'message': 'Descarga completada',
                        'title': title,
                        'download_url': download_url
                    })
                
                return jsonify({
                    'success': False, 
                    'message': f'Archivo no encontrado después del procesamiento. Archivos: {all_files}'
                }), 500

    except Exception as e:
        print(f"Error completo: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download_file/<filename>')
def download_file(filename):
    filepath = os.path.join('downloads', filename)
    print(f"Intentando descargar: {filepath}")
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'success': False, 'message': 'Archivo no encontrado'}), 404

if __name__ == '__main__':
    print("Iniciando servidor...")
    print(f"FFmpeg location: C:\\Users\\LENOVO\\Documents\\descargador\\ffmpeg-8.0.1\\bin")
    app.run(debug=True, port=5000)