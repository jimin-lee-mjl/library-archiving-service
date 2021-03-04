from flask import Blueprint, g, render_template, url_for, redirect

bp = Blueprint('main', __name__)


@bp.route('/')
def dashboard():
    if g.user:
        return render_template('dash.html', username=g.user.username)
    else:
        return redirect(url_for('auth.login'))
