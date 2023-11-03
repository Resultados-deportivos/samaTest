from jinja2 import Environment, FileSystemLoader
from models import *
from flash_messages import *
import os
from http.cookies import SimpleCookie

env = Environment(loader=FileSystemLoader('templates'))
index = env.get_template('index.html')
competiciones = env.get_template('competiciones.html')
equipos = env.get_template('equipos.html')
partidos = env.get_template('eventos.html')
error = env.get_template('error.html')
sign_in = env.get_template('sign-in.html')
sign_up = env.get_template('sign-up.html')
admin = env.get_template('admin.html')
crud = env.get_template('crud.html')

active_sessions = {}
def start_session():
    session_id = os.urandom(16).hex()
    return session_id


def page_index(environ, start_response):
    publicaciones = get_posts()
    comments_list = get_comments()
    response = index.render(publicaciones=publicaciones, comments_list=comments_list, css_name='inicio.css').encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]


def page_competiciones(environ, start_response):
    competiciones_list = get_leagues()
    response = competiciones.render(competiciones_list=competiciones_list, css_name='competiciones.css').encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]


def page_equipos(environ, start_response):
    equipos_list = get_teams()
    response = equipos.render(equipos_list=equipos_list, css_name='equipos.css').encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]


def page_partidos(environ, start_response):
    events = get_events()
    response = partidos.render(events=events, css_name='eventos.css').encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]


def page_sign_in(environ, start_response):
    usuarios_list = get_users(admin=False)
    print(usuarios_list)
    response = sign_in.render(css_name='login.css').encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]

    if environ['REQUEST_METHOD'] == 'POST':
        form_data = parse_post_data(environ)
        email = form_data.get('email')
        password = form_data.get('password')
        print(email, password)

        for user in usuarios_list:
            if user['correo'] == email and user['contrasena'] == password:
                session_id = start_session()
                active_sessions[session_id] = user  # Store user information in the active sessions
                cookie = SimpleCookie()
                cookie["session_id"] = session_id
                start_response('302 Found', [('Location', '/es/inicio')])
                return []
            else:
                print("No se encontró el usuario")

    start_response(status, response_headers)
    return [response]


def page_sign_up(environ, start_response):
    response = sign_up.render(css_name='login.css').encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    if environ['REQUEST_METHOD'] == 'POST':
        form_data = parse_post_data(environ)
        user = form_data.get('usuario')
        email = form_data.get('email')
        password = form_data.get('password')
        re_password= form_data.get('re-password')
        print(email, password)
    start_response(status, response_headers)
    return [response]


def page_admin(environ, start_response):
    usuarios = get_users(admin=True)
    admin_user = None

    if environ['REQUEST_METHOD'] == 'POST':
        form_data = parse_post_data(environ)
        email = form_data.get('email')
        password = form_data.get('password')

        admin_user = next(
            (user for user in usuarios if user['correo'] == email and user['contrasena'] == password and user['admin']),
            True)

    if admin_user:
        add_flash_message('Bienvenido', 'success')  # Add a flash message
        response_headers = [('Location', '/es/admin/crud/')]
        status = '302 Found'
        start_response(status, response_headers)
        return []

    flash_messages = get_flash_messages()  # Retrieve flash messages
    response = admin.render(css_name='login.css', flash_messages=flash_messages, message="No se encontró").encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]
'''
def page_admin(environ, start_response):
    usuarios = get_users(admin=True)
    admin_user = None

    if environ['REQUEST_METHOD'] == 'POST':
        form_data = parse_post_data(environ)
        email = form_data.get('email')
        password = form_data.get('password')

        # Buscar el usuario en la lista de usuarios con "admin" True
        admin_user = next(
            (user for user in usuarios if user['correo'] == email and user['contrasena'] == password and user['admin']),
            True)

    if admin_user:

        response_headers = [('Location', '/es/admin/crud/')]
        status = '302 Found'
        start_response(status, response_headers)
        return []

    response = admin.render(css_name='login.css', message="No se encontró").encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]

'''
def page_crud(environ, start_response):
    response = crud.render().encode('utf-8')
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]


def redirect_inicio(environ, start_response):
    response_headers = [('Location', '/es/inicio')]
    start_response('302 Found', response_headers)
    return []


def parse_post_data(environ):
    from urllib.parse import parse_qs
    data = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
    form_data = parse_qs(data)
    return form_data


def serve_static(environ, start_response, path):
    # Set the appropriate content type for CSS
    if path.endswith('.css'):
        content_type = 'text/css'
    else:
        content_type = 'text/plain'  # Set a default content type for other static files

    try:
        with open('.' + path, 'rb') as file:
            response_body = file.read()
        status = '200 OK'
    except FileNotFoundError:
        response_body = b'File Not Found'
        status = '404 Not Found'

    response_headers = [('Content-type', content_type)]
    start_response(status, response_headers)
    return [response_body]


def serve_static_img(environ, start_response, path):
    # Set the appropriate content type for CSS
    if path.endswith('.png'):
        content_type = 'image/png'
    else:
        content_type = 'text/plain'  # Set a default content type for other static files

    try:
        with open('.' + path, 'rb') as file:
            response_body = file.read()
        status = '200 OK'
    except FileNotFoundError:
        response_body = b'File Not Found'
        status = '404 Not Found'

    response_headers = [('Content-type', content_type)]
    start_response(status, response_headers)
    return [response_body]


def serve_static_js(environ, start_response, path):
    # Set the appropriate content type for JavaScript files
    if path.endswith('.js'):
        content_type = 'application/javascript'
    else:
        content_type = 'text/plain'  # Set a default content type for other static files

    try:
        with open('.' + path, 'rb') as file:
            response_body = file.read()
        status = '200 OK'
    except FileNotFoundError:
        response_body = b'File Not Found'
        status = '404 Not Found'

    response_headers = [('Content-type', content_type)]
    start_response(status, response_headers)
    return [response_body]


def handle_404(environ, start_response):
    response = error.render().encode('utf-8')
    status = '404 Not Found'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [response]
