import  functools
from click.decorators import password_option
from flask import (
    Blueprint,
    flash,
    g,
    render_template,    
    request,
    url_for,
    session,
    redirect
)
#Check verifica las contraseñas y generate las encripta
from werkzeug.security import check_password_hash, generate_password_hash 

from todo.db import get_db


#Blueprint para autenticar
bp = Blueprint('auth', __name__, url_prefix='/auth') 


#FUNCION PARA REGISTRAR USUARIO
@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT id FROM user WHERE username = %s', (username,)
        )

        if not username:
            error = 'Username requerido'

        if not password:
            error = 'Password requerido'

        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)


        if error is None:
            password = generate_password_hash(password)

            c.execute(
                'INSERT INTO user(username, password) VALUES (%s, %s)',
                (username, password)
            )
            db.commit()
            
            return redirect(url_for('auth.login'))

        flash(error)
    
    return render_template('auth/register.html')

 

#FUNCION PARA LOGUEARSE
@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM user WHERE username = %s', (username, )
        )
        user = c.fetchone()

        if user is None:
            error= 'Usuario y/o contraseña invalida'
        
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('todo.index')) 
        
        flash(error)

    return render_template('auth/login.html')

#FUNCION PARA CARGAR AL USUIARIO
@bp.before_app_request
def load_logged_in_user():
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


#Funcion para proteger nuestros endpoint
def login_required(view):
    #Envolvemos la funcion de view con functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view


# FUNCION DE LOGOUT
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))