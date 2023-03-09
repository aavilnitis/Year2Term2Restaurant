from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from packages.extensions import db
from packages.models import MenuItem, User
from customer.customer import customer
from waiter.waiter import waiter
from signup.signup import signup
from login.login import login_view
from kitchen.kitchen import kitchen
from admin.admin import admin
import bcrypt

#if os.path.exists("instance/database.db"):
#    print('is database')
#    os.remove("instance/database.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

app.register_blueprint(customer, url_prefix="/customer")
app.register_blueprint(waiter, url_prefix="/waiter")
app.register_blueprint(signup, url_prefix="/signup")
app.register_blueprint(login_view, url_prefix="/login")
app.register_blueprint(kitchen, url_prefix="/kitchen")
app.register_blueprint(admin, url_prefix="/admin")


@app.route('/', methods = ['POST', 'GET'])
def home():
    if not User.query.filter_by(username='waiter1').first():
        passw = 'waiter'
        waiter = User('waiter', bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt()), 'waiter', None, 1, 10)
        waiter1 = User('waiter1', bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt()), 'waiter', None, 11, 20)
        waiter2 = User('waiter2', bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt()), 'waiter', None, 21, 30)
        waiter3 = User('waiter3', bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt()), 'waiter', None, 31, 40)
        db.session.add(waiter)
        db.session.add(waiter1)
        db.session.add(waiter2)
        db.session.add(waiter3)
        db.session.commit()
        
    if 'user' in session:
        if session['user'] == 'customer':
            return redirect(url_for('customer.home'))
        elif session['user'] == 'waiter':
            return redirect(url_for('waiter.home'))
        else:
            return "smth went wrong"
    else:
        return redirect(url_for("login_view.login"))

    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
