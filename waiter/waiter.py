from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
import functools
from packages.models import MenuItem, Order, db, Ingredient
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
waiter = Blueprint("waiter", __name__, static_folder="static",
                   template_folder="templates")

def split_string(input_string):
    return [word.strip() for word in input_string.split(',')]

def namesToArray(ingredient_names):
    ingredients = []
    for ingredient_name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient:
            ingredients.append(ingredient)
    return ingredients

def waiter_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'waiter':
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper

@waiter.route('/')
@waiter_required
def home():
    return render_template('waiter-home.html')

@waiter.route('view-orders')
@waiter_required
def view_orders():
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    return render_template('waiter-view-order.html', orders = orders, menu_items = menu_items)


@waiter.route('/menu')
@waiter_required
def menu():
    menu_items = MenuItem.query.all()
    return render_template('waiter-menu.html', items=menu_items)


@waiter.route('/add-item', methods=['GET', 'POST'])
@waiter_required
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
        return menu_item.name
    return render_template('add_item.html')

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


# Flask route to confirm order
# Update the status of the order


@waiter.route('/confirm_order/<int:order_id>', methods=['POST'])
@waiter_required
def confirm_order(order_id):
    order = Order.query.get(order_id)
    order.status = "complete"
    db.session.commit()
    return redirect(url_for('waiter.view_orders'))
