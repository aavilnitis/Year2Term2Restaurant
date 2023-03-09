from flask import session, redirect, url_for
import functools
from packages.models import Order, Notification, db
from sqlalchemy import text

def split_string(input_string):
    return [word.strip() for word in input_string.split(',')]

# Populates the database with premade SQL inserts
def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()
            
def change_delivery(order_id, status, table_num, user_id):
    order = Order.query.get(order_id)
    order.delivery_status = status
    
    notif = Notification(user_id,table_num, status)
    db.session.add(notif)
    db.session.commit()
    
def kitchenstaff_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'kitchen_staff':
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            if session.get('user') == 'admin':
                return redirect(url_for('admin.home'))
            if session.get('user') == 'waiter':
                return redirect(url_for('waiter.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper

