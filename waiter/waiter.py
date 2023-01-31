from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
from packages.models import MenuItem, Order, db
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
waiter = Blueprint("waiter", __name__, template_folder = "templates")

@waiter.route('/')
def home():
    return "<h1>Waiter home</h1>"


