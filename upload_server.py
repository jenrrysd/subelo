from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import subprocess
import os

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" type="text/css" href="estilos.css">
                    <title>Subir Archivo</title>
                    <style>
                        /* Estilo opcional para centrar el formulario en la página */
                        body {
                            block: center
                            background-color: #add8e6;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 10vh;
                            margin: 0;
                        }
                         
                         .container {
                            background: white;
                            padding: 30px;
                            border-radius: 10px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            width: 100%;
                            max-width: 500px;
                            text-align: center;
                        }
                         
                        form {
                            text-align: center;
                        }
                    </style>
                    <script>
                        function limpiarArchivo() {
                            // Selecciona el input de tipo file por su nombre y limpia su valor
                            document.getElementsByName("file")[0].value = "";
                        }
                    </script>                    
                </head>
                <body>
                    <div class="container">             
                        <form method="post" enctype="multipart/form-data">
                            <h1>Sube el archivo</h1> 
                            <input name="file" type="file">
                            <input type="submit" value="Subir archivo">
                            <input type="button" value="Limpiar archivo" onclick="limpiarArchivo()">
                        </form>
                    </div>
                </body>
            </html>
        """.encode('utf-8'))

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type, text/html, charset=utf-8'],
                     })

        # Recibe el archivo subido y lo guarda en el directorio actual
        field_item = form['file']
        if field_item.filename:
            file_data = field_item.file.read()
            file_name = field_item.filename
            with open(file_name, "wb") as f:
                f.write(file_data)
            self._set_response()
            self.wfile.write('''
                <div class="container" style="text-align: center; background-color: #add8e7;">
                    El archivo; "{}" Fue subido exitosamente.<br>
                    <input type="button" value="Regresar a la página anterior" onclick="javascript:history.back()"><br>
                </div>
                '''.format(file_name).encode('utf-8'))

        else:
            self._set_response()
            self.wfile.write('''
                <div class="container" style="text-align: center; background-color: #ffcccc;">
                    No se subió ningún archivo.<br>
                    <input type="button" value="Regresar a la página anterior" onclick="javascript:history.back()"><br>
                </div>
            '''.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=7080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    ip_local = subprocess.check_output("ip route | awk '{print $9}' | head -1",shell=True).decode('utf-8').strip()
    ruta = input('Ingresa la ruta donde se guardarán los archivos: ').strip()
    os.chdir(ruta)
    print(f"Los archivos se guardaran en la ruta; {ruta}")
    print(f"Exponiendo httpd en la ip y puerto; {ip_local}:{port}")
    
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
