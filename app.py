from flask import Flask, g, render_template
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def dashboard():
    return render_template('dash.html', username = g.user.username)

# any extensions using app as current_app should be inside
with app.app_context():
    from db import init_db
    init_db()

    import auth
    app.register_blueprint(auth.bp)

if __name__ == '__main__':
    app.run