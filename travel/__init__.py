from dbm.dumb import error

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

# This has to be imported after we declare db as it references db
from .auth import login

def create_app():
    app = Flask(__name__)

    Bootstrap5(app)
    Bcrypt(app)

    app.secret_key = 'somerandomvalue'

    # CONFIG DB and initialise it
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    # CONFIG Image Upload Folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialise the login manager for the app
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    # add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", error=e)

    return app
