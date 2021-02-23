from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

# any extensions using app as current_app should be inside
with app.app_context():
    from db import init_db
    init_db()

    import auth
    app.register_blueprint(auth.bp)

if __name__ == '__main__':
    app.run