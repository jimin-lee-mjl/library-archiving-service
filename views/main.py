from flask import Blueprint, g, render_template, url_for, redirect
from auth import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def dashboard():
    if g.user:
        return render_template('dash.html', username=g.user.username)
    else:
        return redirect(url_for('auth.login'))
