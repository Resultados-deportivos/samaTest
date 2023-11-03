from wsgiref.simple_server import make_server
from views import *


def app(environ, start_response):
    path = environ.get('PATH_INFO')
    # Redirección a /es/inicio si no hay nada en la ruta
    if path == '/':
        return redirect_inicio(environ, start_response)
    # Inicio
    if path == '/es/inicio':
        return page_index(environ, start_response)
    # Competiciones
    elif path == '/es/competiciones':
        return page_competiciones(environ, start_response)
    # Equipos
    elif path == '/es/equipos':
        return page_equipos(environ, start_response)
    # Partidos
    elif path == '/es/partidos':
        return page_partidos(environ, start_response)
    # Sign In
    elif path == '/es/sign-in':
        return page_sign_in(environ, start_response)
    # Sign Up
    elif path == '/es/sign-up':
        return page_sign_up(environ, start_response)
    # Admin
    elif path == '/es/admin':
        return page_admin(environ, start_response)
    # Admin loged
    elif path.startswith('/es/admin/crud/'):
        # Obtener el nombre del usuario de la URL
        return page_crud(environ, start_response)
    # Load CSS
    elif path == '/static/style.css' or path == '/static/inicio.css' or path == '/static/login.css' \
            or path == '/static/eventos.css' or path == '/static/competiciones.css'\
            or path == '/static/equipos.css':
        return serve_static(environ, start_response, path)
    # Load Folder /static/Img
    elif path.startswith('/static/img/'):
        return serve_static_img(environ, start_response, path)
    # Load JS
    elif path.startswith('/static/script.js'):
        return serve_static_js(environ, start_response, path)
    # Do not found
    else:
        return handle_404(environ, start_response)


if __name__ == "__main__":
    host = 'localhost'
    port = 8081
    httpd = make_server(host, port, app)
    print(f"Servidor en http://{host}:{port}")
    httpd.serve_forever()
