from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import User
from packages.extensions import db
import bcrypt

login = Blueprint("Login",__name__,static_folder="static",template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the entered username and password
        username = request.form['username']
        password = request.form['password']

        # Fetch the user from the database based on the entered username
        user = User.query.filter_by(username=username).first()

        # If the user exists, check the entered password against the hashed password in the database
        if user and bcrypt.check_password_hash(user.password, password):
            return redirect(url_for('home'))
        else:
            # Incorrect credentials. Perhaps lock after some tries?
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')
