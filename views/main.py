from flask import Blueprint, g, render_template, url_for, redirect
from auth import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def dashboard():
    rentals = g.user.rentals
    return render_template('dashboard.html', rentals=rentals,
                                             username=g.user.username,
                                             length=len(rentals))
