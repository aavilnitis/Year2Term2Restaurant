from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
from packages.models import MenuItem, Order, db
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
waiter = Blueprint("waiter", __name__, static_folder="static", template_folder="templates")

def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()

@waiter.route('/')
def home():
    return render_template('waiter-home.html')


@waiter.route('/menu')
def menu():
    if MenuItem.query.filter_by(name = "Cheeseburger").first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template('waiter-menu.html', items=menu_items)


@waiter.route('/confirm-new-item')
def confirm_new_item():
    return render_template('waiter-home.html')


# Route to add item into menu
@waiter.route('/add-item')
def additem():
    return render_template('add_item.html')


