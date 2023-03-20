from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
import functools
from packages.models import MenuItem, Order, db, Ingredient, Notification, User
from sqlalchemy.sql import text, and_
from .static.functions.waiter_functions import split_string, populate_menu, waiter_required, add_item, change_delivery, names_to_array

# register customer_view as a Flask Blueprint
waiter = Blueprint("waiter", __name__, static_folder="static",
                   template_folder="templates")


@waiter.route('/')
@waiter_required
def home():
    """Renders the home page for the waiter displaying all notifications that exist for the current waiter according to their table number

    Returns:
        str: The HTML content for the home page template for waiter
    """
    # Gets User.id of current waiter and find the User from database
    waiter = User.query.get(session['user_id'])
    # Gets all notifications for which its table_number is assigned to current waiter
    notifications = Notification.query.filter(
        Notification.table_number >= waiter.table_number_start, Notification.table_number <= waiter.table_number_end).all()
    if notifications:
        return render_template('waiter-home.html', notifications=notifications, waiter=waiter)
    else:
        return render_template('waiter-home.html', notifications=None, waiter=waiter)


@waiter.route('/menu')
@waiter_required
def menu():
    """Checks if a MenuItem exists, if not it will call the populate_menu function to update menu data

    Returns:
        str: The HTML content for the menu page template with all MenuItems
    """
    # Calls populate_menu if there are no MenuItems
    if MenuItem.query.first() == None:
        populate_menu()
    # Query all MenuItems and render menu template
    menu_items = MenuItem.query.all()
    return render_template('waiter-menu.html', menu_items=menu_items)


@waiter.route('/add-item', methods=['GET', 'POST'])
@waiter_required
def addItem():
    """Renders the add-item page and handles form submissionf for adding a new MenuItem to database

    Returns:
        str: The HTML content for for the add-item page, or if form is submitted taken back to menu page
    """
    # If form is submitted, get all submissions
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        ingredient_names = split_string(request.form.get('ingredients'))
        calories = request.form.get('calories')
        type = request.form.get('type')
        picture = request.form.get('picture')
        # Call add_item function to create new MenuItem and redirect to menu page
        add_item(name, price, description,
                 ingredient_names, calories, type, picture)
        return redirect(url_for('waiter.menu'))
    types = db.session.query(MenuItem.type).distinct()
    return render_template('add_item.html', types=types)


@waiter.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
def editItem(item_id):
    """Edits data of an existing MenuItem

    Args:
        item_id (id): The id of the MenuItem in database

    Returns:
        str: The HTML content for menu page after editiing a MenuItem, or renders the edit-item page to allow waiter to edit item
    """
    item = MenuItem.query.get(item_id)
    # Delete the old MenuItem, and replace it with new data
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        ingredient_names = split_string(request.form.get('ingredients'))
        picture = request.form.get('picture')
        # Check if new ingredients are already in database or not
        for ingredient_name in ingredient_names:
            if Ingredient.query.filter_by(name=ingredient_name).first() == None:
                db.session.add(Ingredient(name=ingredient_name))
                db.session.commit()
        ingredients = names_to_array(ingredient_names)
        calories = request.form.get('calories')
        type = request.form.get('type')

        # Creates the new MenuItem and commits new changes to database
        menu_item = MenuItem(name=name, price=price, description=description,
                             ingredients=ingredients, calories=calories, type=type, picture=picture)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('waiter.menu'))

    else:
        types = db.session.query(MenuItem.type).distinct()
        ingredient_save = ""
        for ingredient in item.ingredients:
            ingredient_save = ingredient_save + "," + ingredient.name
        return render_template('waiter-edit_item.html', types=types, item=item, ingredient_save=ingredient_save[1:])


@waiter.route('/remove-item/<int:item_id>', methods=['GET', 'POST'])
@waiter_required
def removeItem(item_id):
    """Gets MenuItem using item_id and removes it from database

    Args:
        item_id (int): The id of the MenuItem to be removed

    Returns:
        flask.Response: Redirects user back to menu
    """
    # Gets MenuItem using item_id, if it exists -  delete it
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('waiter.menu'))


@waiter.route('view-notifications')
@waiter_required
def viewNotifications():
    """This gets all notifications that are associated with the table assignment of current wiater

    Returns:
        str: The HTML content for the notifications page for waiter
    """
    # Gets waiters id from session and filters notifcation using their table number
    waiter = User.query.get(session['user_id'])
    notifications = Notification.query.filter(
        Notification.table_number >= waiter.table_number_start, Notification.table_number <= waiter.table_number_end).all()
    return render_template('waiter-view-notifications.html', notifications=notifications)


@waiter.route('/remove-notification/<int:notif_id>', methods=['POST'])
@waiter_required
def removeNotification(notif_id):
    """This will remove the notification from the database that has popped up on home page

    Args:
        notif_id (int): The id of the notification being removed from database from home page

    Returns:
        flask.Response: Redirects waiter to home page
    """
    notification = Notification.query.filter_by(id=notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('waiter.home'))


@waiter.route('/remove-notification-page/<int:notif_id>', methods=['POST'])
@waiter_required
def removeNotificationPage(notif_id):
    """This will remove the notification from the database and will no longer show on notifications page

    Args:
        notif_id (int): The id of the notification being removed from database

    Returns:
        flask.Response: Redirects waiter to notifications page with updated notifications from database
    """
    notification = Notification.query.filter_by(id=notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('waiter.viewNotifications'))


@waiter.route('view-orders')
@waiter_required
def viewOrders():
    """Gets all Orders thats customers have placed at tables assigned to current waiter

    Returns:
        str: The HTML content of view-order page for waiter
    """
    # Gets id of current waiter from session
    waiter = User.query.get(session['user_id'])

    # Gets all customers that are at tables assigned to current waiter and stores their ids in a list
    users = User.query.filter(User.table_number >= waiter.table_number_start,
                              User.table_number <= waiter.table_number_end).all()
    user_ids = []
    for user in users:
        user_ids.append(user.id)

    # Iterates through all orders and add orders with user_id in user_ids list to a orders list
    orders = []
    all_orders = Order.query.all()
    for order in all_orders:
        if order.user_id in user_ids:
            orders.append(order)
    menu_items = MenuItem.query.all()

    return render_template('waiter-view-order.html', orders=orders, menu_items=menu_items, users=users)


@waiter.route('/confirm_order/<int:order_id>', methods=['POST'])
@waiter_required
def confirmOrder(order_id):
    """This changes the status of an Order a customer has placed to confirmed

    Args:
        order_id (int): The id of the Order being confirmed

    Returns:
        flask.Response: Redirects waiter to updated vieworders page
    """
    order = Order.query.get(order_id)
    order.status = "confirmed"
    db.session.commit()
    return redirect(url_for('waiter.viewOrders'))


@waiter.route('/cancel_order/<int:order_id>', methods=['POST'])
@waiter_required
def cancelOrder(order_id):
    """This checks if the order exists, then it first deletes its ordermenuitems and then the order from database

    Args:
        order_id (int): The id of the Order to be deleted

    Returns:
        flask.Response: Redirects waiter to updated view orders page
    """
    order = Order.query.get(order_id)
    # If Order exists, delete OrderMenuItems associated and then the Order
    if order:
        for menu_item in order.order_menu_items:
            db.session.delete(menu_item)
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('waiter.viewOrders'))


@waiter.route('/change-delivery/<int:order_id>/<string:status>', methods=['POST'])
@waiter_required
def changeDelivery(order_id, status):
    """This calls the change_delivery function to update the delivery_status of the Order

    Args:
        order_id (int): The id of the Order for which delivery_status is being updated
        status (enum): The status which is being updated 

    Returns:
        flask.Response: Redirects waiter to updated view orders page with changes made in change_delivery
    """
    # Calls change_delivery function
    change_delivery(order_id, status)
    return redirect(url_for('waiter.viewOrders'))
