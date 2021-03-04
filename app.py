from flask import Flask
from flask_bootstrap import Bootstrap
from config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    Bootstrap(app)


    # any extensions using app as current_app should be inside
    with app.app_context():
        from db import init_db
        import auth
        from views import book
        from views import personal
        from views import main
        
        init_db()
        app.register_blueprint(auth.bp)
        app.register_blueprint(book.bp)
        app.register_blueprint(personal.bp)
        app.register_blueprint(main.bp)

        # from library import create_library
        # create_library() 
    
    return app

