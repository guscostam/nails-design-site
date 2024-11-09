from flask import Blueprint, render_template, redirect, url_for, session

system_index_bp = Blueprint('system_index', __name__)

@system_index_bp.route('/scheduling')
def scheduling():
    if 'username' in session:
        return render_template('scheduling.html')
    else:
        return redirect(url_for('login.index_login'))

@system_index_bp.route('/products')
def products():
    if 'username' in session:
        return render_template('products.html')
    else:
        return redirect(url_for('login.index_login'))
