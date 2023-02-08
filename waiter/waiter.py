from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
from packages.models import MenuItem, Order, db
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
waiter = Blueprint("waiter", __name__, static_folder="static", template_folder="templates")


@waiter.route('/')
def home():
    return render_template('waiter-home.html')


@waiter.route('/menu')
def menu():
    menu_items = MenuItem.query.all()
    return render_template('waiter-menu.html', items=menu_items)


# Flask route to cancel an order
# Delete the order from the database
@waiter.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    db.delete(order)
    db.commit()
    return redirect(url_for('orders'))

# Flask route to confirm order 
# Update the status of the order
@waiter.route('/confirm_order/<int:order_id>', methods=['POST'])
def confirm_order(order_id):
    order = Order.query.get(order_id)
    order.status = "complete"
    db.session.commit()
    return redirect(url_for('orders'))

# Route to add item into menu
@waiter.route('/add_item.html')
def additem():
    name = request.form['Name']
    price = request.form['Price']
    des = request.form['Des']    # Description
    ingre = request.form['Ing']  # Ingredients
    cal = request.form['Cal']    # calories
    type = request.form['Type']
    form_data = MenuItem(name, price, des, type)
    db.session.add(form_data)   # add Item into db
    db.session.commit()
    return render_template('add_item.html')

