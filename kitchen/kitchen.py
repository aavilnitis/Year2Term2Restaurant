from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text
from waiter.static.functions.waiter_functions import split_string, populate_menu, change_delivery

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

# HOME
@kitchen.route('/')
def home():
    notifications = Notification.query.filter_by(notification_type = 'new-order').all()
    if notifications:
        return render_template('kitchen-home.html', notifications = notifications)
    else:
        return render_template('kitchen-home.html', notifications = None)


# NOTIFICATIONS
@kitchen.route('view-notifications')
def viewNotifications():
    waiter = User.query.get(session['user_id'])
    notifications = Notification.query.filter(Notification.table_number >= waiter.table_number_start, Notification.table_number <= waiter.table_number_end).all()
    return render_template('waiter-view-notifications.html', notifications = notifications)

@kitchen.route('/remove-notification/<int:notif_id>', methods = ['POST'])
def removeNotification(notif_id):
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('waiter.home'))

@kitchen.route('/remove-notification-page/<int:notif_id>', methods = ['POST'])
def removeNotificationPage(notif_id):
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('waiter.viewNotifications'))



# ORDERS
@kitchen.route('view-orders')
def viewOrders():
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('kitchen-view-order.html', orders = orders, menu_items = menu_items, users = users)

# Flask route to confirm order
# Update the status of the order
@kitchen.route('/confirm_order/<int:order_id>', methods=['POST'])
def confirmOrder(order_id):
    order = Order.query.get(order_id)
    order.status = "confirmed"
    db.session.commit()
    return redirect(url_for('waiter.viewOrders'))

# Flask route to cancel an order
# Delete the order from the database
@kitchen.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancelOrder(order_id):
    order = Order.query.get(order_id)
    if order:
        for menu_item in order.order_menu_items:
            db.session.delete(menu_item)
        db.session.delete(order)
        db.session.commit() 
    return redirect(url_for('waiter.viewOrders'))

# Flask route to mark order as delivered
# Update the status of the order
@kitchen.route('/change-delivery/<int:order_id>/<string:status>', methods=['POST'])
def changeDelivery(order_id, status):
    change_delivery(order_id, status)
    return redirect(url_for('waiter.viewOrders'))
    


