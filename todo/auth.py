import  functools #Esto es un set de funciones que podemos utilizar cuando estamos construyendo aplicaciones
from click.decorators import password_option #Es un set de funciones que podemos utilizar cuando estamos creando aplicaciones
from flask import (
    Blueprint, #Nos permite crear blueprints/modulos configurables 
    flash, #Es una pequeña funcion de manera generica a nuestra plantilla
    g, #Una variable general de Flask
    render_template, #Para renderizar plantillas
    request, #Para recibir elementos por medio de los metodos HTTP (formularios)
    url_for, #Sirve para crear URL
    session, #Es para mantener una referencia del usuario que encuentra interactuando con nuestra aplicacion
    redirect #Este modulo es para redirigir a las funciones o a las plantillas
)
from werkzeug.security import check_password_hash, generate_password_hash #Check verifica las contraseñas y generate las encripta

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  #Blueprint de autenticacion 


#FUNCION PARA REGISTRAR USUARIO

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST': #Validamos que el metodo que nosotros enviamos en el formulario sea POST
        username = request.form['username']
        password = request.form['password']
        db, c = get_db() #Traemos la base de datos
        error = None
        c.execute( #Ejecutamos la consulta
            'SELECT id FROM user WHERE username = %s', (username,)
        )

        if not username: #Si el usuario no ingresa un username haga esto
            error = 'Username requerido'

        if not password: #Si el usuario no ingresa una contraseña haga esto
            error = 'Password requerido'

        elif c.fetchone() is not None: #Si el usuario ingresa un usuario existente
            error = 'Usuario {} se encuentra registrado.'.format(username)


        if error is None: #Si el usuario ingresa todo bien
            password = generate_password_hash(password)

            c.execute(
                'INSERT INTO user(username, password) VALUES (%s, %s)',
                (username, password)
            )
            db.commit()
            
            return redirect(url_for('auth.login'))

        flash(error) #Enviamos mensaje de error, en caso de que haya algun error
    
    return render_template('auth/register.html')

 
#FUNCION PARA LOGUEARSE
@bp.route('/login', methods=['GET','POST']) #Definimos ruta para el login
def login():
    if request.method == 'POST': #Validamos que el metodo que nosotros enviamos en el formulario sea POST
        username = request.form['username']
        password = request.form['password']
        db, c = get_db() #Llamamos a la funcion get_db() para manipular la base de datos
        error = None
        c.execute(
            'SELECT * FROM user WHERE username = %s', (username, )
        )
        user = c.fetchone() #Aqui le damos el valor extraido de username a la variable user

        if user is None: #Aqui verificamos si el valor de user no existe, entonces devolvemos error
            error= 'Usuario y/o contraseña invalida'
        
        elif not check_password_hash(user['password'], password): #Aqui consultamos si la contraseña que nosotros le estamos pasando es la misma que tenemos registrada en la base de datos

            error = 'Usuario y/o contraseña invalida'

        if error is None: #Si no hay ningun error, quiere decir que todo salío bien
            session.clear() #Limpiamos la sesion
            session['user_id'] = user['id'] #Creamos una variable llamada user_id, a la cual le asignaremos el id del user que consultamos

            return redirect(url_for('todo.index')) #retornamos el index que seria el inicio 
        
        flash(error) #Mostramos un mensaje, si es que en algun momento hubo un error

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user(): #funcion para cargar al usuiario
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()
        db.commit()


def login_required(view): #Funcion para proteger nuestros endpoint
    @functools.wraps(view) #Envolvemos la funcion de view con functools
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))