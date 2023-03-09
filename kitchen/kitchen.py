from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
kitchen = Blueprint("kitchen", __name__, static_folder="static", template_folder="templates")

def kitchenstaff_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'kitchen_staff':
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            else: 
                return "You do not have permission to view this page"
        return func(*args, **kwargs)
    return wrapper

@kitchen.route('/')
@kitchenstaff_required
def home():
    orders = Order.query.filter_by(status = 'incomplete').all()
    return render_template("kitchen-home.html", orders = orders)

@kitchen.route('/order/ready', methods = ['POST'])
@kitchenstaff_required 
def order_ready():
    order_id = request.form.get(order_id)
    order = Order.query.get(order_id)
    if order:
        order.delivery_status = 'ready'
        db.session.commit()
    else:
        return jsonify({'message': 'Order not found.'})
    


