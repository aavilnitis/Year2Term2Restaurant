from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
import functools
from packages.models import MenuItem, Order, db, Ingredient, Notification, User
from sqlalchemy.sql import text
from .static.functions.waiter_functions import split_string, populate_menu, waiter_required, add_item

# register customer_view as a Flask Blueprint
waiter = Blueprint("waiter", __name__, static_folder="static",
                   template_folder="templates")

# HOME
@waiter.route('/')
@waiter_required
def home():
    notifications = Notification.query.all()
    if notifications:
        return render_template('waiter-home.html', notifications = notifications, help_needed = True)
    else:
        return render_template('waiter-home.html', help_needed = False)



# MENU
@waiter.route('/menu')
@waiter_required
def menu():
    if MenuItem.query.first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template('waiter-menu.html', menu_items=menu_items)

@waiter.route('/add-item', methods=['GET', 'POST'])
@waiter_required
def addItem():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        ingredient_names = split_string(request.form.get('ingredients'))
        calories = request.form.get('calories')
        type = request.form.get('type')
        picture = request.form.get('picture')
        add_item(name,price,description,ingredient_names,calories,type, picture)
        return redirect(url_for('waiter.menu'))
    types = db.session.query(MenuItem.type).distinct()
    return render_template('add_item.html', types = types)

@waiter.route('/remove-item/<int:item_id>', methods = ['GET','POST'])
@waiter_required
def removeItem(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit() 
    return redirect(url_for('waiter.menu'))



# NOTIFICATIONS
@waiter.route('view-notifications')
@waiter_required
def view_notifications():
    notifications = Notification.query.all()
    return render_template('waiter-view-notifications.html', notifications = notifications)

@waiter.route('/remove-notification/<int:notif_id>', methods = ['POST'])
@waiter_required
def remove_notification(notif_id):
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('waiter.home'))



# ORDERS
@waiter.route('view-orders')
@waiter_required
def view_orders():
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('waiter-view-order.html', orders = orders, menu_items = menu_items, users = users)

# Flask route to confirm order
# Update the status of the order
@waiter.route('/confirm_order/<int:order_id>', methods=['POST'])
@waiter_required
def confirm_order(order_id):
    order = Order.query.get(order_id)
    order.status = "complete"
    db.session.commit()
    return redirect(url_for('waiter.view_orders'))

# Flask route to cancel an order
# Delete the order from the database
@waiter.route('/cancel_order/<int:order_id>', methods=['POST'])
@waiter_required
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if order:
        for menu_item in order.order_menu_items:
            db.session.delete(menu_item)
        db.session.delete(order)
        db.session.commit() 
    return redirect(url_for('waiter.view_orders'))

    




    






    








