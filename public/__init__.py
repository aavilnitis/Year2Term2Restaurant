from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .customer_view import customer_view
    app.register_blueprint(customer_view, url_prefix='/')

    create_database(app)

    return app


def create_database(app):
    if not path.exists('public/' + DB_NAME):
        with app.app_context():
            db.create_all(app=app)
        print('Created Database!')
