from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, db
from sqlalchemy.sql import text

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
        flash('User created succesfully', category='success')
        return render_template("signup.html")
    return render_template("signup.html")


