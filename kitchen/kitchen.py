from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
kitchen = Blueprint("kitchen", __name__, static_folder="static", template_folder="templates")

@kitchen.route('/')
def home():
    return render_template("kitchen-home.html")

