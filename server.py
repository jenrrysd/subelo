from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os
import sys
import cgi


class FileUploadHandler(BaseHTTPRequestHandler):
    def _set_response(self, content_type='text/html; charset=utf-8'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _serve_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, f"File {filepath} not found")

    def do_GET(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if self.path == '/':
            self._set_response()
            self._serve_file(os.path.join(base_dir, 'index.html'))
        elif self.path == '/style.css':
            self._set_response('text/css')
            self._serve_file(os.path.join(base_dir, 'style.css'))
        elif self.path == '/script.js':
            self._set_response('application/javascript')
            self._serve_file(os.path.join(base_dir, 'script.js'))
        elif self.path == '/favicon.png':
            self._set_response('image/png')
            favicon_path = os.path.join(base_dir, 'favicon.png')
            if os.path.exists(favicon_path):
                self._serve_file(favicon_path)
            else:
                self.send_error(404, "favicon no encontrado")
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        try:
<<<<<<< HEAD
            content_type, pdict = cgi.parse_header(self.headers['content-type'])
            
            if content_type == 'multipart/form-data':
                # Parsear el formulario multipart
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Procesar cada archivo
                uploaded_files = []
                for field in form.list:
                    if field.filename:
                        # Guardar el archivo
                        filename = os.path.basename(field.filename)
                        with open(filename, 'wb') as f:
                            f.write(field.file.read())
                        uploaded_files.append(filename)
                
                self._set_response()
                files_list = "<br>".join([f'"{f}"' for f in uploaded_files])
=======
            content_length = int(self.headers['Content-Length'])
            content_type = self.headers['Content-Type']

            if not content_type.startswith('multipart/form-data'):
                raise Exception("Formato no soportado")

            boundary = content_type.split('boundary=')[1].encode()
            data = self.rfile.read(content_length)

            parts = data.split(b'--' + boundary)
            uploaded_files = []

            for part in parts:
                if b'Content-Disposition: form-data; name="file"; filename="' in part:
                    # Extraer nombre del archivo
                    filename_start = part.find(b'filename="') + 10
                    filename_end = part.find(b'"', filename_start)
                    filename = part[filename_start:filename_end].decode()
                    filename = os.path.basename(filename)

                    if filename:
                        # Extraer contenido del archivo
                        file_content_start = part.find(b'\r\n\r\n') + 4
                        file_content_end = part.find(
                            b'\r\n--', file_content_start)
                        if file_content_end == -1:
                            file_content_end = len(part) - 2

                        file_content = part[file_content_start:file_content_end]

                        # Guardar archivo
                        with open(filename, 'wb') as f:
                            f.write(file_content)
                        uploaded_files.append(filename)

            self._set_response()
            if uploaded_files:
                files_list = ', '.join(uploaded_files)
>>>>>>> 72b289b (archivos modificados)
                response = f'''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Archivos Subidos</title>
                        <link rel="stylesheet" href="/style.css">
                    </head>
                    <body>
                        <div class="container">
<<<<<<< HEAD
                            <p>{len(uploaded_files)} archivo(s) subido(s) exitosamente:</p>
                            <p>{files_list}</p>
=======
                            <p>Archivos "{files_list}" subidos exitosamente.</p>
>>>>>>> 72b289b (archivos modificados)
                            <div class="button-container">
                                <button class="action-button" onclick="window.location.reload()">Volver</button>
                            </div>
                        </div>
                    </body>
                    </html>
                '''
<<<<<<< HEAD
                self.wfile.write(response.encode('utf-8'))
            else:
                raise Exception("Formato no soportado")
=======
            else:
                response = '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Error</title>
                        <link rel="stylesheet" href="/style.css">
                    </head>
                    <body>
                        <div class="container">
                            <p>No se seleccionaron archivos válidos.</p>
                            <div class="button-container">
                                <button class="action-button" onclick="history.back()">Volver</button>
                            </div>
                        </div>
                    </body>
                    </html>
                '''
            self.wfile.write(response.encode('utf-8'))
>>>>>>> 72b289b (archivos modificados)

        except Exception as e:
            self._set_response()
            error_response = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Error</title>
                    <link rel="stylesheet" href="/style.css">
                    <link rel="icon" type="image/png" href="/imagenes/favicon.png">
                </head>
                <body>
                    <div class="container">
                        <p>Error al subir archivos: {str(e)}</p>
                        <div class="button-container">
                            <button class="action-button" onclick="history.back()">Volver</button>
                        </div>
                    </div>
                </body>
                </html>
            '''
            self.wfile.write(error_response.encode('utf-8'))


def run_server(port=7080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FileUploadHandler)

    # Obtener IP local
    try:
        ip_local = subprocess.check_output(
            "hostname -I | awk '{print $1}'", shell=True).decode('utf-8').strip() or "localhost"
    except:
        ip_local = "localhost"

    # Solicitar ruta de guardado
    while True:
        ruta = input(
            'Ingresa la ruta donde se guardarán los archivos: ').strip()
        if os.path.isdir(ruta):
            os.chdir(ruta)
            break
        else:
            print(
                f"Error: La ruta '{ruta}' no existe. Por favor ingresa una ruta válida.")

    print(f"\n● Servidor activo en: http://{ip_local}:{port}")
    print(f"● Archivos se guardarán en: {os.getcwd()}")
    print("● Presiona Ctrl+C para detener el servidor\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7080
    run_server(port)
<<<<<<< HEAD


=======
>>>>>>> 72b289b (archivos modificados)
