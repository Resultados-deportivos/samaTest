from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os
from faker import Faker
import random
import requests

load_dotenv()  # Esto funciona para no tener credenciales guardadas en el propio codigo

#api_url = "http://18.234.195.81/basket/"
api_url = "http://localhost:8080/basket/"

url = URL.create("postgresql", username=os.getenv('USERNAME_DATABASE'), password=os.getenv('PASSWORD_DATABASE'),
                 host=os.getenv('HOST_DATABASE'), database=os.getenv('NAME_DATABASE'))
engine = create_engine(url)

Base = declarative_base()


class Publicaciones(Base):
    __tablename__ = 'publicaciones'
    id = Column(Integer, primary_key=True)
    img = Column(String(255))
    titulo = Column(String(255))
    descripcion = Column(String(255))


class Eventos(Base):
    __tablename__ = 'eventos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    fecha = Column(Date)
    horainicio = Column(Time)
    horafin = Column(Time)
    temporada = Column(String(10))
    idestadios = Column(Integer, ForeignKey('estadios.id'))
    idliga = Column(Integer, ForeignKey('ligas.id'))


class Jugadores(Base):
    __tablename__ = 'jugadores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    fechanacim = Column(Date)
    equipoid = Column(Integer, ForeignKey('equipos.id'))
    altura = Column(String(30))
    peso = Column(String(10))
    numero = Column(Integer)


class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    contrasena = Column(String(255))
    correo = Column(String(255))
    admin = Column(Boolean)


class Ligas(Base):
    __tablename__ = 'ligas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    logo = Column(String(255))
    temporadaactual = Column(Integer)
    youtube = Column(String(255))
    web = Column(String(255))


class Estadios(Base):
    __tablename__ = 'estadios'
    id = Column(Integer, primary_key=True)
    # nombre = Column(String)
    localizacion = Column(String(255))
    capacidad = Column(Integer)


class Equipos(Base):
    __tablename__ = 'equipos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    ciudad = Column(String(255))
    logo = Column(String(255))
    id_liga = Column(Integer, ForeignKey('ligas.id'))


class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    publicacionid = Column(Integer, ForeignKey('publicaciones.id'))
    usuarioid = Column(Integer, ForeignKey('usuarios.id'))
    likecount = Column(Integer)


class Registros(Base):
    __tablename__ = "registros"
    id = Column(Integer, primary_key=True)
    eventoid = Column(Integer, ForeignKey('eventos.id'))
    jugadorid = Column(Integer, ForeignKey('jugadores.id'))
    accion = Column(String(255))
    minuto = Column(Integer)


class Comentarios(Base):
    __tablename__ = "comentarios"
    id = Column(Integer, primary_key=True)
    idusuario = Column(Integer, ForeignKey('usuarios.id'))
    publicacionid = Column(Integer, ForeignKey('publicaciones.id'))
    descripcion = Column(String(255))


class Puntos(Base):
    __tablename__ = "puntos"
    id = Column(Integer, primary_key=True)
    eventoid = Column(Integer, ForeignKey('eventos.id'))
    puntos = Column(String)


def insert_player_data(ID, name, lastname, fecha_nacim, teamid, height, weight, number):
    Session = sessionmaker(bind=engine)
    sesion = Session()
    nuevo_registro = Jugadores(id=ID, nombre=name, apellido=lastname, fechanacim=fecha_nacim, equipoid=teamid,
                               altura=height, peso=weight, numero=number)
    sesion.add(nuevo_registro)
    sesion.commit()
    sesion.close()


def insert_stadium_data(location, capacity):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Estadios(localizacion=location, capacidad=capacity)
    session.add(new_register)
    session.commit()


def insert_teams_data(ID, name, city, brand, id_league):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Equipos(id=ID, nombre=name, ciudad=city, logo=brand, id_liga=id_league)
    session.add(new_register)
    session.commit()


def insert_league_data(ID, name, brand, actual_season, yt, web_url):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Ligas(id=ID, nombre=name, logo=brand, temporadaactual=actual_season, youtube=yt, web=web_url)
    session.add(new_register)
    session.commit()


def insert_events_data(ID, name, event_date, init_hour, end_hour, season, stadium_id, league_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Eventos(id=ID, nombre=name, fecha=event_date, horainicio=init_hour, horafin=end_hour,
                           temporada=season, idestadios=stadium_id, idliga=league_id)
    session.add(new_register)
    session.commit()


def insert_coments_data(user_id, publication_id, description):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Comentarios(idusuario=user_id, publicacionid=publication_id, descripcion=description)
    session.add(new_register)
    session.commit()


def insert_likes_data(publication_id, user_id, like_count):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Likes(publicacionid=publication_id, usuarioid=user_id, likecount=like_count)
    session.add(new_register)
    session.commit()


def insert_publications_data(pub_img, pub_title, pub_desc):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Publicaciones(img=pub_img, titulo=pub_title, descripcion=pub_desc)
    session.add(new_register)
    session.commit()


def insert_registers_data(game_id, jugador_id, action, minute):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Registros(partidoid=game_id, jugadorid=jugador_id, accion=action, minuto=minute)
    session.add(new_register)
    session.commit()


def insert_users_data(name, password, email, isAdmin):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Usuarios(nombre=name, contrasena=password, correo=email, admin=isAdmin)
    session.add(new_register)
    session.commit()


def insert_points_data(event_id, points):
    Session = sessionmaker(bind=engine)
    session = Session()
    new_register = Puntos(eventoid=event_id, puntos=points)
    session.add(new_register)
    session.commit()


def generate_fake_data():
    fake = Faker()

    # Esta libreria Faker se utiliza para generar registros fictcios
    player_records = []

    for i in range(11, 200):
        nombre = fake.first_name_male()
        apellido = fake.last_name()
        fechanacim = fake.date_of_birth(minimum_age=18, maximum_age=40)
        equipoid = random.randint(1, 20)  # Equipos ficticios del 1 al 10
        altura = f"{random.randint(5, 7)} ft {random.randint(0, 11)} in"
        peso = f"{random.randint(60, 100)}kg"
        numero = random.randint(1, 99)
        player_records.append((i, nombre, apellido, fechanacim, equipoid, altura, peso, numero))

    for record in player_records:
        insert_player_data(*record)


def get_events(fecha=None, temporada=None):
    '''
        La fecha tiene que ser en el formato que esté en la base de datos que estes utilizando
    '''
    endpoint_name = "events"
    endpoint_params = {}
    # Para filtrar por fecha
    if fecha is not None and temporada is None:
        endpoint_params['fecha'] = fecha
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    # Para filtrar por temporada
    elif fecha is None and temporada is not None:
        endpoint_params['temporada'] = temporada
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    # Para devolver todo sin filtro
    else:
        try:
            # Send a GET request to the API
            response = requests.get(api_url + endpoint_name)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                weather_data = response.json()

                return weather_data
            else:
                print(f"API request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_players(id_team=None):
    if id is not None:
        endpoint_name_by_id = f"players?equipoid={id_team}"

        try:
            response = requests.get(api_url + endpoint_name_by_id)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Status code: {response.status_code}")
        except Exception as exception:
            print(f"Error: {exception}")
    else:
        endpoint_name_all = "players"
        try:
            response = requests.get(api_url + endpoint_name_all)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Status code: {response.status_code}")
        except Exception as exception:
            print(f"Error: {exception}")
    return None


def get_teams(id=None, id_liga=None):
    endpoint_name = "teams"
    endpoint_params = {}
    if id is not None and id_liga is None:
        endpoint_params['id'] = id
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and id_liga is not None:
        endpoint_params['id_liga'] = id_liga
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_stadiums(id=None, localizacion=None):
    endpoint_name = "stadiums"
    endpoint_params = {}
    if id is not None and localizacion is None:
        endpoint_params['id'] = id
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and localizacion is not None:
        endpoint_params['localizacion'] = localizacion
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_comments(idusuario=None, publicacionid=None):
    endpoint_name = "comments"
    endpoint_params = {}
    if idusuario is not None and publicacionid is None:
        endpoint_params['idusuario'] = idusuario
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif idusuario is None and publicacionid is not None:
        endpoint_params['publicacionid'] = publicacionid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_leagues(id=None):
    endpoint_name = "leagues"
    endpoint_params = {}
    if id is not None:
        endpoint_params['id'] = id
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_likes(usuarioid=None, publicacionid=None):
    endpoint_name = "likes"
    endpoint_params = {}
    if usuarioid is not None and publicacionid is None:
        endpoint_params['usuarioid'] = usuarioid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif usuarioid is None and publicacionid is not None:
        endpoint_params['publicacionid'] = publicacionid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif usuarioid is not None and publicacionid is not None:
        endpoint_params['usuarioid'] = usuarioid
        endpoint_params['publicacionid'] = publicacionid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_posts(id=None, titulo=None):
    '''
        Al filtrar por titulo mostrará todas las publicaciones que en su titulo contengan la cadena insertada
        como parámetro
    '''
    endpoint_name = "posts"
    endpoint_params = {}
    if id is not None and titulo is None:
        endpoint_params['id'] = id
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and titulo is not None:
        endpoint_params['titulo'] = "%" + (titulo) + "%"
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_points(eventoid=None):
    '''
        Estos son los resultados filtrados por eventoid
    '''
    endpoint_name = "points"
    endpoint_params = {}
    if eventoid is not None:
        endpoint_params['eventoid'] = eventoid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_logs(id=None, eventoid=None, jugadorid=None):
    '''
        Para obtener los registros podemos filtrar por id, eventoid, jugadorid, u obtenerlos todos
    '''
    endpoint_name = "logs"
    endpoint_params = {}
    if id is not None and eventoid is None and jugadorid is None:
        endpoint_params['id'] = id
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and eventoid is not None and jugadorid is None:
        endpoint_params['eventoid'] = eventoid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and eventoid is None and jugadorid is not None:
        endpoint_params['jugadorid'] = jugadorid
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


def get_users(id=None, nombre=None, correo=None, admin=None):
    '''
        Podemos filtrar por cada parametro, por la combinacion de "correo" y "admin" o
        sin parámetros
        admin(Boolean)
    '''
    endpoint_name = "users"
    endpoint_params = {}
    if id is not None and nombre is None and correo is None and admin is None:
        endpoint_params['id'] = id
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and nombre is not None and correo is None and admin is None:
        endpoint_params['nombre'] = nombre
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and nombre is None and correo is not None and admin is None:
        endpoint_params['correo'] = correo
        try:
            response = requests.get(api_url + endpoint_name, params=endpoint_params)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and nombre is None and correo is None and admin is not None:
        endpoint_params['admin'] = admin
        try:
            if isinstance(admin, bool):
                response = requests.get(api_url + endpoint_name, params=endpoint_params)
                if response.status_code == 200:
                    data = response.json()
                    return data
                else:
                    print(f"Response code: {response.status_code}")
            else:
                print(f"Error: El valor introducido no es Boolean")
                return None
        except Exception as e:
            print(f"Error: {e}")
    elif id is None and nombre is None and correo is not None and admin is not None:
        endpoint_params['correo'] = correo
        endpoint_params['admin'] = admin
        try:
            if isinstance(admin, bool):
                response = requests.get(api_url + endpoint_name, params=endpoint_params)
                if response.status_code == 200:
                    data = response.json()
                    return data
                else:
                    print(f"Response code: {response.status_code}")
            else:
                print(f"Error: El valor introducido no es Boolean")
                return None
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            response = requests.get(api_url + endpoint_name)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Response code: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    return None


if __name__ == '__main__':

    print(get_users())