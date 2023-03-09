from flask import session, url_for, redirect
from packages.models import Ingredient, Notification, db
import functools
from sqlalchemy import text

def split_string(input_string):
    return [word.strip() for word in input_string.split(',')]

def names_to_array(ingredient_names):
    ingredients = []
    for ingredient_name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient:
            ingredients.append(ingredient)
    return ingredients

# Populates the database with premade SQL inserts
def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()

def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'admin':
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            if session.get('user') == 'waiter':
                return redirect(url_for('waiter.home'))
            if session.get('user') == 'kitchen_staff':
                return redirect(url_for('kitchen.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper

def check_cleared_notifs():
    if 'cleared_notifs' not in session:
        session['cleared_notifs'] = []
    notifications = []
    notifications_database = Notification.query.all()
    cleared_notifs = session['cleared_notifs']
    for notification in notifications_database:
        if notification.id not in cleared_notifs:
            notifications.append(notification)
    return notifications