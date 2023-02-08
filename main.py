from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from packages.extensions import db
from packages.models import MenuItem
from customer.customer import customer
from waiter.waiter import waiter
from signup.signup import signup


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

app.register_blueprint(customer, url_prefix="/")
app.register_blueprint(waiter, url_prefix="/waiter")
app.register_blueprint(signup, url_prefix="/signup")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
