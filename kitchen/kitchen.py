from flask import Blueprint, render_template, redirect, session, url_for
from packages.models import MenuItem, Order, User, Notification, db
from sqlalchemy.sql import not_
from kitchen.static.functions.kitchen_functions import change_delivery, change_delivery, kitchenstaff_required

# register kitchen view as a Flask Blueprint
kitchen = Blueprint("kitchen", __name__, static_folder="static", template_folder="templates")


# HOME
@kitchen.route('/')
@kitchenstaff_required
def home():
    """Queries database for all new-order type notifications and renders Kitchen staff home page
        template that displays said notifications

    Returns:
        str: The HTML content of the waiter-home template
    """
    notifications = Notification.query.filter_by(notification_type = 'new-order').all()
    if notifications:
        return render_template('kitchen-home.html', notifications = notifications)
    else:
        return render_template('kitchen-home.html', notifications = None)


# NOTIFICATIONS
@kitchen.route('view-notifications')
@kitchenstaff_required
def viewNotifications():
    notifications = Notification.query.filter_by(notification_type = 'new-order').all()
    return render_template('kitchen-view-notifications.html', notifications = notifications)

@kitchen.route('/remove-notification/<int:notif_id>', methods = ['POST'])
@kitchenstaff_required
def removeNotification(notif_id):
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('kitchen.home'))

@kitchen.route('/remove-notification-page/<int:notif_id>', methods = ['POST'])
@kitchenstaff_required
def removeNotificationPage(notif_id):
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('kitchen.viewNotifications'))



# ORDERS
@kitchen.route('view-orders')
@kitchenstaff_required
def viewOrders():
    orders = Order.query.filter(not_(Order.delivery_status == 'delivered')).all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('kitchen-view-order.html', orders = orders, menu_items = menu_items, users = users)

# Flask route to confirm order
# Update the status of the order
@kitchen.route('/confirm_order/<int:order_id>', methods=['POST'])
@kitchenstaff_required
def confirmOrder(order_id):
    order = Order.query.get(order_id)
    order.status = "confirmed"
    db.session.commit()
    return redirect(url_for('waiter.viewOrders'))

# Flask route to cancel an order
# Delete the order from the database
@kitchen.route('/cancel_order/<int:order_id>', methods=['POST'])
@kitchenstaff_required
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
@kitchen.route('/change-delivery/<int:order_id>/<string:status>/<int:user_id>', methods=['POST'])
@kitchenstaff_required
def changeDelivery(order_id, status, user_id):
    customer = User.query.get(user_id)
    table_num = customer.table_number
    change_delivery(order_id, status, table_num, user_id)
    return redirect(url_for('kitchen.viewOrders'))
    


