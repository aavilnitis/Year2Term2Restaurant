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
