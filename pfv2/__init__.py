from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
# from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "you-will-never-guess"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    
    # from .models import Account, Category, Budget, Incoming, Expense 
    from .models import Account, AccountType, Budget

    # Blueprint for generic views in our app
    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    # Blueprint for admin view our app
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
   
    #print(app.url_map)  

    return app
