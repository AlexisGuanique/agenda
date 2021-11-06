from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort #Cuando algun usuario intente modificar algun todo que no le pertenezca, nosotros le enviamos el mensaje de abort

from todo.auth import login_required #Funcion que nos permite proteger todos nuestros endpoints
from todo.db import get_db #Importamos nuestra base de datos


bp = Blueprint('todo', __name__) #Blueprint para nuestros todos

@bp.route('/')  #Esta funcion es para listar todos los todos (registros)
@login_required
def index():
    db, c = get_db()
    c.execute(
        'SELECT t.id, t.description, u.username, t.completed, t.create_at FROM todo as t JOIN user as u on t.create_by = u.id where t.create_by = %s ORDER BY create_at desc', (g.user['id'],)
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)



@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
             error = 'Descripción requerida'
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into todo(description, completed, create_by)'
                'values(%s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.create_by, t.create_at, u.username from todo t join user u on t.create_by = u.id WHERE t.id = %s;',
        (id,)
    )
    todo = c.fetchone()

    if todo is None:
        abort(404, 'El todo de id {} no existe'.format(id))
    return todo

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error = None

        if not description:
            error = 'La descripción es requerida.'

        if error is not None:
            flash(error)

        else:
            db, c = get_db()
            c.execute(
                'update todo set description = %s, completed = %s where id = %s and create_by = %s;',
                (description, completed, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))


    return render_template('todo/update.html', todo=todo)



@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from todo where id = %s and create_by = %s', (id, g.user['id'])
    )
    db.commit()

    return redirect(url_for('todo.index'))

