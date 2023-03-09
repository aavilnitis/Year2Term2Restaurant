from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import Ingredient, MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text

from waiter.waiter import namesToArray, split_string

# register customer_view as a Flask Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/')
def home():
    return render_template("admin-home.html")

@admin.route('/kitchen')

def kitchen():
    return render_template("kitchen.html")

@admin.route('/addkitchen', methods=['GET', 'POST'])
def add_kitchen():
    if request.method == 'POST':
        username = str(request.form.get('username'))
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