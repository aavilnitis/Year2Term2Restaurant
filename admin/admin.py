from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db, Ingredient, Notification
import functools
from sqlalchemy.sql import text
import bcrypt
from waiter.static.functions.waiter_functions import names_to_array, split_string, populate_menu

# register customer_view as a Flask Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

def checkClearedNotifs():
    if 'cleared_notifs' not in session:
        session['cleared_notifs'] = []
    notifications = []
    notifications_database = Notification.query.all()
    cleared_notifs = session['cleared_notifs']
    for notification in notifications_database:
        if notification.id not in cleared_notifs:
            notifications.append(notification)
    return notifications
    
# HOME
@admin.route('/')
def home():
    notifications = checkClearedNotifs()
    if len(notifications) > 0:
        return render_template('admin-home.html', notifications = notifications)
    else:
        return render_template('admin-home.html')
    
# NOTIFICATIONS
@admin.route('view-notifications')
def viewNotifications():
    notifications = checkClearedNotifs()
    return render_template('admin-view-notifications.html', notifications = notifications)

@admin.route('/remove-notification-page/<int:notif_id>', methods = ['POST'])
def removeNotificationPage(notif_id):
    cleared_notifs = session['cleared_notifs']
    cleared_notifs.append(notif_id)
    session['cleared_notifs'] = cleared_notifs
    return redirect(url_for('admin.viewNotifications'))

@admin.route('/remove-notification/<int:notif_id>', methods = ['POST'])
def removeNotification(notif_id):
    cleared_notifs = session['cleared_notifs']
    cleared_notifs.append(notif_id)
    session['cleared_notifs'] = cleared_notifs
    return redirect(url_for('admin.home'))
    

    
# ORDERS
@admin.route('view-orders')
def viewOrders():
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('admin-view-order.html', orders = orders, menu_items = menu_items, users = users)


# MENU 
@admin.route('/menu')
def menu():
    if MenuItem.query.first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template('admin-menu.html', menu_items=menu_items)

@admin.route('/admin-add-item', methods=['GET', 'POST'])
def addItem():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        ingredient_names = split_string(request.form.get('ingredients'))
        for ingredient_name in ingredient_names:
            if Ingredient.query.filter_by(name=ingredient_name).first() == None:
                db.session.add(Ingredient(name = ingredient_name))
                db.session.commit()
        ingredients = names_to_array(ingredient_names)
        calories = request.form.get('calories')
        type = request.form.get('type')
        
        menu_item = MenuItem(name = name, price = price, description = description, ingredients = ingredients, calories = calories, type = type)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('admin.menu'))
    types = db.session.query(MenuItem.type).distinct()
    return render_template('admin-add_item.html', types = types)

@admin.route('/remove-item/<int:item_id>', methods = ['GET','POST'])
def removeItem(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit() 
    return redirect(url_for('admin.menu'))


# ADD WAITER/KITCHEN
@admin.route('add-new-staff', methods=['GET', 'POST'])
def addNewKitchen():
    if request.method == 'POST':
        staff_type = request.form['staff_type']
        if staff_type == 'Kitchen Staff':
            return redirect(url_for('admin.kitchen'))
        elif staff_type == 'Waiter':
            return redirect(url_for('admin.add_waiter'))
    return render_template('add-new-staff.html')


@admin.route('/add-waiter', methods=['GET', 'POST'])
def add_waiter():
    users = User.query.filter_by(user_type='customer').all()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        table_number_start = request.form.get('table_number_start')
        table_number_end = request.form.get('table_number_end')
        waiter = User(username = username, password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), user_type = 'waiter', table_number_start = table_number_start, table_number_end = table_number_end)
        db.session.add(waiter)
        db.session.commit()
        return redirect(url_for('admin.home'))
    return render_template("add-waiter.html", users=users)