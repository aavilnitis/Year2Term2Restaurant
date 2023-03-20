from flask import session, redirect, url_for
import functools
from packages.models import Order, Notification, db
from sqlalchemy import text

def split_string(input_string):
    """Splits a comma separated string into a list of strings 

    Args:
        input_string (str): The comma separated string to be split

    Returns:
        List[str]: The list of the split strings
    """
    return [word.strip() for word in input_string.split(',')]

# Populates the database with premade SQL inserts
def populate_menu():
    """Populated menu with data from the SQL file
    """
    # Open the SQL file and iterate through each line and execute the SQL statement
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()
            
def change_delivery(order_id, status, table_num, user_id):
    """This changes the status field of the Order in the database

    Args:
        order_id (int): The id of the Order for which status is being changed
        status (enum): The status of the Order that is being updated
        table_num (int): the Table number of the customer who's order is being updated 
        user_id (int): The id of the user who's order is being updated
    """
    # Change order status
    order = Order.query.get(order_id)
    order.delivery_status = status
    
    # Send notification to waiter and manager that order is 'preparing' or 'ready'
    notif = Notification(user_id,table_num, status)
    db.session.add(notif)
    db.session.commit()
    
def kitchenstaff_required(func):
    """Checks if current User is a Kitchen staff member, if not redirects User to corresponding home page

    Args:
        func (function): The function to be decorated

    Returns:
        function: The decorated function
    """
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

