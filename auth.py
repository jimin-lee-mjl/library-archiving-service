from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
    g,
    current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from db import db, User
from form import RegisterForm, LoginForm
from error_msg import AuthError

bp = Blueprint('auth', __name__, url_prefix='/auth')


@current_app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        g.user = user


def login_required(f):
    @wraps(f)
    def check_login(*args, **kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return check_login


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # vaildate_on_sumit() : form.is_submitted + form.vaild - only when the form is submitted
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        exist_user = User.query.filter_by(email=email).first()

        if exist_user:
            flash(AuthError.email.inavailable, 'auth_error')
        else:
            hashed_pw = generate_password_hash(password, method="sha256")
            new_user = User(
                username=username,
                email=email,
                password=hashed_pw
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session.pop('user_id', None)
        email = form.email.data
        password = form.password.data
        exist_user = User.query.filter_by(email=email).first()

        if not exist_user:
            flash(AuthError.email.no_match, 'auth_error')
        elif not check_password_hash(exist_user.password, password):
            flash(AuthError.password.inavailable, 'auth_error')
        else:
            session['user_id'] = exist_user.id
            return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return render_template('auth/login_required.html')