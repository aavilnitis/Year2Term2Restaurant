from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import User
from packages.extensions import db
import bcrypt

# register customer_view as a Flask Blueprint
signup = Blueprint("signup", __name__, static_folder="static", template_folder="templates")

@signup.route('/', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) < 5:
            flash('Username must be longer than 5 characters!', category='error')
            return redirect(url_for('signup.sign_up'))
        if len(password) < 5:
            flash('Password must be longer than 5 characters!', category='error')
            return redirect(url_for('signup.sign_up'))
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username, password, 'customer')
        db.session.add(user)
        db.session.commit()
        flash('User created succesfully', category='success')
        session['user'] = 'customer'
        session['user_id'] = user.id
        return redirect(url_for("customer.table_number"))
    return render_template("signup.html")


