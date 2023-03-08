from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/')
def home():
    return render_template("admin-home.html")


@admin.route('/add-waiter')
def add_waiter():
    users = User.query.filter_by(user_type='customer').all()
    return render_template("add-waiter.html", users=users)
