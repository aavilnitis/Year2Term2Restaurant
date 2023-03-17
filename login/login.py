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
                # If the entered password is correct, set session variables and redirect to appropriate page based on user type
                session['user'] = found_user.user_type
                session['user_id'] = found_user.id
                print(found_user.id)
                # Redirect the user to the appropriate page based on user type
                if found_user.user_type == 'customer':
                    return redirect(url_for('customer.table_number'))
                elif found_user.user_type == 'waiter':
                    return redirect(url_for('waiter.home'))
                elif found_user.user_type == 'kitchen_staff':
                    return redirect(url_for('kitchen.home'))
                elif found_user.user_type == 'admin':
                    return redirect(url_for('admin.home'))
                else:
                    # Something went wrong if we reach this point, so flash an error message and redirect to the login page
                    flash('Something went wrong!', category='error')
                    return redirect(url_for('login_view.login'))
            else:
                # If the password is incorrect, flash an error message and redirect to the login page
                flash('Incorrect password', category='error')
                return redirect(url_for('login_view.login'))
        else:
            # If the user is not found, flash an error message and redirect to the login page
            flash('User not found', category='error')
            return redirect(url_for('login_view.login'))
        
     # If the request method is GET, request render the login template    
    return render_template("login.html")
    
   