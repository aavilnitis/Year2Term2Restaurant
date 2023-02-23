from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import User
from packages.extensions import db
import bcrypt

login_view = Blueprint("login_view",__name__,static_folder="static",template_folder="templates")

@login_view.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the entered username and password
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Fetch the user from the database based on the entered username
        found_user = User.query.filter_by(username=username).first()

        # If the user exists, check the entered password against the hashed password in the database
        if found_user:
            if bcrypt.checkpw(password, found_user.password):
                session['user'] = found_user.user_type
                session['user_id'] = found_user.id
                print(found_user.id)
                return redirect(url_for('customer.table_number'))
            else:
                flash('Incorrect password', category='error')
                return redirect(url_for('login_view.login'))
        else:
            flash('User not found', category='error')
            return redirect(url_for('login_view.login'))
        
        
    return render_template("login.html")
    