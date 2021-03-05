from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SECRET_KEY, DB_URI

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Bootstrap(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # any extensions using app as current_app should be inside
    with app.app_context():
        import auth
        from views import book
        from views import archive
        from views import main
        
        db.create_all()
        app.register_blueprint(auth.bp)
        app.register_blueprint(book.bp)
        app.register_blueprint(archive.bp)
        app.register_blueprint(main.bp)

        # from library import create_library
        # create_library() 
    
    return app

