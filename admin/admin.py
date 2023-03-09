from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db, Ingredient, Notification
import functools
from sqlalchemy.sql import text
import bcrypt

from waiter.waiter import namesToArray, split_string

# register customer_view as a Flask Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


def split_string(input_string):
    return [word.strip() for word in input_string.split(',')]

def namesToArray(ingredient_names):
    ingredients = []
    for ingredient_name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient:
            ingredients.append(ingredient)
    return ingredients

# Populates the database with premade SQL inserts
def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()

def waiter_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'waiter': # Consider changing to 'admin' once 
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper

@admin.route('/')
def home():
    notifications = Notification.query.all()
    if notifications:
        return render_template('admin-home.html', notifications = notifications, help_needed = True)
    else:
        return render_template('admin-home.html', help_needed = False)
    
@admin.route('add-new-staff', methods=['GET', 'POST'])
def add_new_staff():
    if request.method == 'POST':
        staff_type = request.form['staff_type']
        if staff_type == 'Kitchen Staff':
            return redirect(url_for('admin.kitchen'))
        elif staff_type == 'Waiter':
            return redirect(url_for('admin.add_waiter'))
    return render_template('add-new-staff.html')
    
@admin.route('/remove-notification/<int:notif_id>', methods = ['POST'])
def remove_notification(notif_id):
    notification = Notification.query.filter_by(id = notif_id).first()
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('admin.home'))

@admin.route('view-notifications')
def view_notifications():
    notifications = Notification.query.all()
    return render_template('waiter-view-notifications.html', notifications = notifications)

@admin.route('/customer_helped/<int:notification_id>', methods=['POST'])
def customer_helped(notification_id):
    notification = Notification.query.get(notification_id)
    notification.status = "helped"
    db.session.commit()
    return redirect(url_for('admin.view_notifications'))
    
@admin.route('view-orders')
def view_orders():
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    users = User.query.all()
    return render_template('waiter-view-order.html', orders = orders, menu_items = menu_items, users = users)


@admin.route('/menu')
def menu():
    if MenuItem.query.first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template('waiter-menu.html', menu_items=menu_items)

@admin.route('/remove-item/<int:item_id>', methods = ['GET','POST'])
def remove_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit() 
    return redirect(url_for('admin.menu'))
    


@admin.route('/add-item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        ingredient_names = split_string(request.form.get('ingredients'))
        for ingredient_name in ingredient_names:
            if Ingredient.query.filter_by(name=ingredient_name).first() == None:
                db.session.add(Ingredient(name = ingredient_name))
                db.session.commit()
        ingredients = namesToArray(ingredient_names)
        calories = request.form.get('calories')
        type = request.form.get('type')
        
        menu_item = MenuItem(name = name, price = price, description = description, ingredients = ingredients, calories = calories, type = type)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('admin.menu'))
    types = db.session.query(MenuItem.type).distinct()
    return render_template('add_item.html', types = types)

# Flask route to cancel an order
# Delete the order from the database


@admin.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if order:
        for menu_item in order.order_menu_items:
            db.session.delete(menu_item)
        db.session.delete(order)
        db.session.commit() 
    return redirect(url_for('admin.view_orders'))


# Flask route to confirm order
# Update the status of the order


@admin.route('/confirm_order/<int:order_id>', methods=['POST'])
def confirm_order(order_id):
    order = Order.query.get(order_id)
    order.status = "complete"
    db.session.commit()
    return redirect(url_for('admin.view_orders'))


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

@admin.route('/kitchen')
def kitchen():
    return render_template("kitchen.html")

@admin.route('/addkitchen', methods=['GET', 'POST'])
def add_kitchen():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        kitchen = User(username,password,'kitchen_staff')
        db.session.add(kitchen)
        db.session.commit()
        return render_template('admin-home.html')
    return render_template('kitchen.html')

@admin.route('/add-item', methods=['GET', 'POST'])
def add_item():
    types = db.session.query(MenuItem.type).distinct()
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        ingredient_names = split_string(request.form.get('ingredients'))
        for ingredient_name in ingredient_names:
            if Ingredient.query.filter_by(name=ingredient_name).first() == None:
                db.session.add(Ingredient(name = ingredient_name))
                db.session.commit()
                ingredients = namesToArray(ingredient_names)
                calories = request.form.get('calories')
                type = request.form.get('type')
                menu_item = MenuItem(name = name, price = price, 
                description = description, 
        ingredients = ingredients, 
        calories = calories, type = type)
        db.session.add(menu_item)
        db.session.commit()
        return redirect(url_for('waiter.menu'))
    return render_template('add_item.html',types = types)

@admin.route('/remove-item/<int:item_id>', methods = ['GET','POST'])
def remove_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit() 
    return redirect(url_for('waiter.menu'))