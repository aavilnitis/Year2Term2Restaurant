from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/')
def home():
    return render_template("admin-home.html")


@admin.route('/add-waiter', methods=['GET', 'POST'])
def add_waiter():
    users = User.query.filter_by(user_type='customer').all()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        table_number_start = request.form.get('table_number_start')
        table_number_end = request.form.get('table_number_end')
        waiter = User(username = username, password = password, user_type = 'waiter', table_number_start = table_number_start, table_number_end = table_number_end)
        db.session.add(waiter)
        db.session.commit()
        return redirect(url_for('admin.home'))
    return render_template("add-waiter.html", users=users)

@admin.route('/kitchen')
def kitchen():
    return render_template("kitchen.html")

@admin.route('/kitchen', methods=['GET', 'POST'])
def add_kitchen():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        kitchen = User(username,password,'kitchen_staff')
        db.session.add(kitchen)
        db.session.commit()
        return render_template('admin-home.html')
    return render_template('kitchen.html')