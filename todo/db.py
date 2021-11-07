import mysql.connector
import click #Herramienta que nos permite configurar los comandos en la terminal
from flask import current_app, g 
from flask.cli import with_appcontext #Sirve para ejecutar el script de nuestra base de datos
from .schema import instructions


# Funcion para conectar con nuestra base de datos
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database= current_app.config['DATABASE'],
        )
        g.c = g.db.cursor(dictionary=True)
    #Aqui cada vez que finalice el if devolvemos la base de datos y el cursor
    return g.db, g.c

#Funcion para cerrar la base de datos
def close_db(e=None): 
    db = g.pop('db', None)
    if db is not None:
        db.close()

#Esta fucion la utilizaremos para realizar las instrucciones de sql que le vamos a pasar
def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit()


@click.command('init-db')
#Esto nos permite ingresar a las variables de entorno como la host, username, password y database
@with_appcontext


#Con esta funcion ejecutamos nuestro script desde la terminal de comandodos
def init_db_command():
    init_db()
    click.echo('Base da datos inicializada') #Esto es para indicarnos que nuestro script a corrido con exito



def init_app(app): #Esta es la funcion que va a realizar el cierre de la db cuando haya terminando de realizar la consulta

    app.teardown_appcontext(close_db) #Este metodo ejecuta funciones, las cuales se las pasamos como argumento, lo utilizamos para cerrar la conexion a nuestra base de datos con la funcion close_db
    
    app.cli.add_command(init_db_command) #Aqui le pasamos la funcion que va a ejecutar




