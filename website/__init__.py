from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CHS'
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345678@localhost/Supermarket'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)
    

    from.auth import auth
    from.views import views
    from .model import UserDetails,StoreUser 


    app.register_blueprint(auth)
    app.register_blueprint(views)

    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return UserDetails.query.get(int(id)) or StoreUser.query.get(int(id))

    
    return app

def create_database(app):
    with app.app_context():
        # db.drop_all()
        db.create_all()