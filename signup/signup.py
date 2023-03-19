from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import User
from packages.extensions import db
import bcrypt
# register customer_view as a Flask Blueprint
signup = Blueprint("signup", __name__, static_folder="static", template_folder="templates")

@signup.route('/', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # get all existing customers' usernames from the database
        users = User.query.filter_by(user_type='customer').all()
        usernames = []
        for user in users:
            usernames.append(user.username)
        # get new username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')
         # validate the username and password
        if len(username) < 5:
            flash('Username must be longer than 5 characters!', category='error')
            return redirect(url_for('signup.sign_up'))
        if username in usernames:
            flash('Username already taken!', category='error')
            return redirect(url_for('signup.sign_up'))
        if len(password) < 5:
            flash('Password must be longer than 5 characters!', category='error')
            return redirect(url_for('signup.sign_up'))
         # hash the password
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
         # create a new customer with the validated username and hashed password
        user = User(username, password, 'customer')
        db.session.add(user)
        db.session.commit()
        # set the session variables for the new customer
        flash('User created succesfully', category='success')
        session['user'] = 'customer'
        session['user_id'] = user.id
        # redirect to the next page, which is the table number selection page for the customer
        return redirect(url_for("customer.table_number"))
     # render the sign-up page if the request method is GET
    return render_template("signup.html")


