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
    """Queries the database for all new-order type notifications and renders the kitchen-view-notifications 
        template displaying said notifications with an option to dismiss them.

    Returns:
        str: The HTML content of the kitchen-view-notifications template.
    """
    notifications = Notification.query.filter_by(notification_type = 'new-order').all()
    return render_template('kitchen-view-notifications.html', notifications = notifications)

@kitchen.route('/remove-notification/<int:notif_id>', methods = ['POST'])
@kitchenstaff_required
def removeNotification(notif_id):
    """Removes a notification from kitchen staff home page.

    Args:
        notif_id (id): The id of the Notification to remove

    Returns:
        flask.Response: A redirect response to the kitchen staff home page
    """
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('kitchen.home'))

@kitchen.route('/remove-notification-page/<int:notif_id>', methods = ['POST'])
@kitchenstaff_required
def removeNotificationPage(notif_id):
    """Removes a notification from kitchen staff notifications page.

    Args:
        notif_id (id): The id of the Notification to remove

    Returns:
        flask.Response: A redirect response to the kitchen staff notifications page
    """
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('kitchen.viewNotifications'))



# ORDERS
@kitchen.route('view-orders')
@kitchenstaff_required
def viewOrders():
    """Queries the database for all orders that have not yet been delivered (are still active)
        and renders the kitchen-view-orders template displaying said orders.

    Returns:
        str: The HTML content of the kitchen-view-orders template.
    """
    orders = Order.query.filter(not_(Order.delivery_status == 'delivered')).all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('kitchen-view-order.html', orders = orders, menu_items = menu_items, users = users)


# Flask route to mark order as delivered
# Update the status of the order
@kitchen.route('/change-delivery/<int:order_id>/<string:status>/<int:user_id>', methods=['POST'])
@kitchenstaff_required
def changeDelivery(order_id, status, user_id):
    """Changes delivery status of an order by calling change_delivery and then 
        redirects the kitchen staff member back to the orders page

    Args:
        order_id (id): The id of the Order which needs to be modified
        status (enum): The status to which order delivery status needs to be changed to
        user_id (_type_): The id of the customer who placed the order

    Returns:
        flask.Response: A redirect response to the kitchen staff orders page
    """
    customer = User.query.get(user_id)
    table_num = customer.table_number
    change_delivery(order_id, status, table_num, user_id)
    return redirect(url_for('kitchen.viewOrders'))
    


