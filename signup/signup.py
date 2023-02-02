from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
from packages.models import MenuItem, Order, db
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
signup = Blueprint("signup", __name__, static_folder="static", template_folder="templates")

@signup.route('/')
def home():
    return render_template("signup.html")


