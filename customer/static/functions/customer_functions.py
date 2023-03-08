from flask import session, url_for, redirect
from packages.models import db
import functools
from sqlalchemy import text

# Creates an empty array as a session directory
def create_cart():
    session['cart'] = []

# Populates the database with premade SQL inserts
def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()
            
def customer_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'customer':
            if session.get('user') == 'waiter':
                return redirect(url_for('waiter.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper