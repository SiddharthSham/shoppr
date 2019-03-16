from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from shopper.auth import login_required
from shopper.db import get_db

bp = Blueprint('main', __name__)

def get_item(id):
    post = get_db().execute(
        'SELECT id, item_name, cost'
        ' FROM list'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Item id {0} doesn't exist.".format(id))

    return post

@bp.route('/')  
@login_required
def index():
    db = get_db()
    items = db.execute(
        'SELECT id, item_name, cost'
        ' FROM list'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('shopper/index.html', list=items)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    """Create a new item"""
    if request.method == 'POST':
        item = request.form['item']
        cost = request.form['cost']
        error = None

        if not item:
            error = 'Item is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO list (item_name, cost)'
                ' VALUES (?, ?)',
                (item, cost)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('shopper/add.html')

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Edit an item"""
    item = get_item(id)

    if request.method == 'POST':
        item = request.form['item']
        cost = request.form['cost']
        error = None

        if not item:
            error = 'Item name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE list SET item_name = ?, cost = ? WHERE id = ?',
                (item, cost, id)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('shopper/edit.html', items=item)

@bp.route('/<int:id>/drop')
@login_required
def drop(id):
    """Delete an item.

    Ensures that the item exists 
    """
    get_item(id)
    db = get_db()
    db.execute('DELETE FROM list WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('main.index'))

@bp.route('/checkout')  
@login_required
def checkout():
    db = get_db()
    selected = request.form.getlist('selected')
    for item in selected:
        db.execute(
            'UPDATE list SET selected = 1 WHERE id = ?',
            (item,)
        )
        db.commit()
    selected = db.execute('SELECT * FROM list WHERE selected = 1').fetchall()
    return redirect(url_for('main.view'))


@bp.route('/view')  
@login_required
def view():
    db = get_db()
    items = db.execute(
        'SELECT id, item_name, cost, quantity'
        ' FROM final'
        ' ORDER BY id DESC'
    ).fetchall()
    return render_template('shopper/view.html', list=items)