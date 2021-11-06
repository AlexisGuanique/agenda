import os
from flask import Flask
from flask.templating import render_template

def create_app(): #Esta funcion nos permitira hacer testing o crear varias instancias de nuestra aplicacion
    app = Flask(__name__) #Todas las aplicaciones son unas instancia de la clase Flask, por eso este objeto e smuy importante

    app.config.from_mapping( #From_mapping nos va a permitir definir variables de entorno que despues las utilizaremos en nuestra a aplicacion

        SECRET_KEY = 'mikey', #Es una llave que se va a utilizar para poder definir las sesiones en nuestra app
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'), #Este es el host donde se encuentra mi base de datos
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'), #Contraseña para ingresar a nuestra base de datos
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'), #Mi usuario para ingresar a la base de datos
        DATABASE = os.environ.get('FLASK_DATABASE'), #Nombre de la base de datos
    )

    from . import db #Aqui llamamos nuestro archivo de base de datos
    db.init_app(app)


    from . import auth #Aqui importamos el blueprint de autenticacion
    from . import todo #Aqui el Blueprint de todo

    app.register_blueprint(auth.bp) #Blueprint de autenticacion
    app.register_blueprint(todo.bp)



    @app.route('/')
    def hola():
        return render_template('auth/register.html')


    return app #Debemos retornoar nuestra app

