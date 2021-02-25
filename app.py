from flask import Flask, g, render_template, url_for, redirect
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def dashboard():
    if g.user:
        return render_template('dash.html', username=g.user.username)
    else:
        return redirect(url_for('auth.login'))


# any extensions using app as current_app should be inside
with app.app_context():
    from db import init_db
    init_db()

    import auth
    app.register_blueprint(auth.bp)

    import book
    app.register_blueprint(book.bp)

    import book_api
    app.register_blueprint(book_api.bp)

    # from library import create_library
    # create_library()


if __name__ == '__main__':
    app.run
