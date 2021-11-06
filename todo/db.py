import mysql.connector
import click #Click es una herrramienta que nos servira para utilizar comandos en la terminal, lo utilizaremos para crear nuestras tablas y la relacion entre ellos
from flask import current_app, g 
from flask.cli import with_appcontext #Sirve para ejecutar el script de nuestra base de datos
from .schema import instructions

def get_db(): #Conectamos a la base de datos, get en español significa obtener
    if 'db' not in g: #Dentro de la variable g vamos a meter a la base de datos (db) y al cursor (c)
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database= current_app.config['DATABASE'],
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c #Aqui cada vez que finalice el if devolvemos la base de datos y el cursor

def close_db(e=None): #Funcion para cerrar la base de datos
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(): #Esta fucion la utilizaremos para realizar las instrucciones de sql que le vamos a pasar
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit()


@click.command('init-db') #Aqui indicamos el comando que utilizaremos para ejecutar la base de datos en la terminal
@with_appcontext #Esto nos permite ingresar a las variables de entorno como la host, username, password y database

def init_db_command(): #Con esta funcion ejecutamos nuestro script desde la terminal de comandodos
    init_db()
    click.echo('Base da datos inicializada') #Esto es para indicarnos que nuestro script a corrido con exito



def init_app(app): #Esta es la funcion que va a realizar cuando este terminando de realizar la consulta

    app.teardown_appcontext(close_db) #Este metodo ejecuta funciones, las cuales se las pasamos como argumento, lo utilizamos para cerrar la conexion a nuestra base de datos con la funcion close_db
    
    app.cli.add_command(init_db_command) #Aqui le pasamos la funcion que va a ejecutar




