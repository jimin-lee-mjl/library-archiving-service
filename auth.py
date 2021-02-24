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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeat_pw = request.form['repeat_pw']
        exist_user = User.query.filter_by(email=email).first()

        if not password == repeat_pw:
            error_msg = '비밀번호가 다릅니다.'
            flash(error_msg)
        elif exist_user:
            error_msg = "이미 존재하는 이메일입니다."
            flash(error_msg)
        else:
            hashed_pw = generate_password_hash(password, method="sha256")
            new_user = User(
                username=username,
                email=email,
                password=hashed_pw
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        email = request.form['email']
        password = request.form['password']
        exist_user = User.query.filter_by(email=email).first()

        if not exist_user:
            error_msg = "존재하지 않는 사용자입니다."
            flash(error_msg)
        elif not check_password_hash(exist_user.password, password):
            error_msg = "비밀번호가 틀렸습니다."
            flash(error_msg)
        else:
            session['user_id'] = exist_user.id
            return redirect(url_for('dashboard'))

    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    return render_template('login_required.html')