from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os
import sys


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
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            boundary = self.headers.get_boundary()
            remainbytes = content_length
            line = self.rfile.readline()
            remainbytes -= len(line)
            if not boundary.encode() in line:
                raise Exception("Content does not begin with boundary")

            line = self.rfile.readline()  # Content-Disposition
            remainbytes -= len(line)
            filename = line.decode().split('filename="')[-1].split('"')[0]
            filename = os.path.basename(filename)

            # Saltar headers intermedios
            while line.strip():
                line = self.rfile.readline()
                remainbytes -= len(line)

            # Leer el contenido del archivo
            with open(filename, 'wb') as out_file:
                preline = self.rfile.readline()
                remainbytes -= len(preline)
                while remainbytes > 0:
                    line = self.rfile.readline()
                    remainbytes -= len(line)
                    if boundary.encode() in line:
                        preline = preline.rstrip(b'\r\n')
                        out_file.write(preline)
                        break
                    else:
                        out_file.write(preline)
                        preline = line

            self._set_response()
            response = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Archivo Subido</title>
                    <link rel="stylesheet" href="/style.css">
                </head>
                <body>
                    <div class="container">
                        <p>Archivo "{filename}" subido exitosamente.</p>
                        <div class="button-container">
                            <button class="action-button" onclick="window.location.reload()">Volver</button>
                        </div>
                    </div>
                </body>
                </html>
            '''
            self.wfile.write(response.encode('utf-8'))

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
                </head>
                <body>
                    <div class="container">
                        <p>Error al subir archivo: {str(e)}</p>
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


# from http.server import BaseHTTPRequestHandler, HTTPServer
# import cgi
# import subprocess
# import os
# import sys


# class FileUploadHandler(BaseHTTPRequestHandler):
#     def _set_response(self, content_type='text/html; charset=utf-8'):
#         self.send_response(200)
#         self.send_header('Content-type', content_type)
#         self.end_headers()

#     def _serve_file(self, filepath):
#         try:
#             with open(filepath, 'rb') as f:
#                 self.wfile.write(f.read())
#         except FileNotFoundError:
#             self.send_error(404, f"File {filepath} not found")

#     def do_GET(self):
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         if self.path == '/':
#             self._set_response()
#             self._serve_file(os.path.join(base_dir, 'index.html'))
#         elif self.path == '/style.css':
#             self._set_response('text/css')
#             self._serve_file(os.path.join(base_dir, 'style.css'))
#         elif self.path == '/script.js':
#             self._set_response('application/javascript')
#             self._serve_file(os.path.join(base_dir, 'script.js'))
#         else:
#             self.send_error(404, "Not Found")

# ######################
#     def do_POST(self):
#         try:
#             content_length = int(self.headers['Content-Length'])
#             form = cgi.FieldStorage(
#                 fp=self.rfile,
#                 headers=self.headers,
#                 environ={'REQUEST_METHOD': 'POST',
#                          'CONTENT_TYPE': self.headers['Content-Type'],
#                          'CONTENT_LENGTH': content_length})

#             file_item = form['file']
#             if file_item.filename:
#                 filename = os.path.basename(file_item.filename)
#                 with open(filename, 'wb') as f:
#                     while True:
#                         chunk = file_item.file.read(8192)
#                         if not chunk:
#                             break
#                         f.write(chunk)

#                 self._set_response()
#                 response = f'''
#                     <!DOCTYPE html>
#                     <html>
#                     <head>
#                         <meta charset="UTF-8">
#                         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                         <title>Archivo Subido</title>
#                         <link rel="stylesheet" href="/style.css">
#                     </head>
#                     <body>
#                         <div class="container">
#                             <p>Archivo "{filename}" subido exitosamente.</p>
#                             <div class="button-container">
#                                 # <button class="action-button" onclick="history.back()">Volver</button>
#                                 <button class="action-button" onclick="window.location.reload()">Volver</button>
#                             </div>
#                         </div>
#                     </body>
#                     </html>
#                 '''
#                 self.wfile.write(response.encode('utf-8'))
#             else:
#                 raise Exception("No file selected")

#         except Exception as e:
#             self._set_response()
#             error_response = f'''
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                     <meta charset="UTF-8">
#                     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                     <title>Error</title>
#                     <link rel="stylesheet" href="/style.css">
#                 </head>
#                 <body>
#                     <div class="container">
#                         <p>Error al subir archivo: {str(e)}</p>
#                         <div class="button-container">
#                             <button class="action-button" onclick="history.back()">Volver</button>
#                         </div>
#                     </div>
#                 </body>
#                 </html>
#             '''
#             self.wfile.write(error_response.encode('utf-8'))
# ###################


# def run_server(port=7080):
#     server_address = ('', port)
#     httpd = HTTPServer(server_address, FileUploadHandler)

#     # Obtener IP local
#     try:
#         ip_local = subprocess.check_output(
#             "hostname -I | awk '{print $1}'", shell=True).decode('utf-8').strip() or "localhost"
#     except:
#         ip_local = "localhost"

#     # Solicitar ruta de guardado
#     while True:
#         ruta = input(
#             'Ingresa la ruta donde se guardarán los archivos: ').strip()
#         if os.path.isdir(ruta):
#             os.chdir(ruta)
#             break
#         else:
#             print(
#                 f"Error: La ruta '{ruta}' no existe. Por favor ingresa una ruta válida.")

#     print(f"\n● Servidor activo en: http://{ip_local}:{port}")
#     print(f"● Archivos se guardarán en: {os.getcwd()}")
#     print("● Presiona Ctrl+C para detener el servidor\n")

#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         print("\nServidor detenido manualmente")


# if __name__ == "__main__":
#     # import sys
#     port = int(sys.argv[1]) if len(sys.argv) > 1 else 7080
#     run_server(port)
