from flask import Blueprint

customer_view = Blueprint('customer_view', __name__)


@customer_view.route('/')
def home():
    return "<h1>Home route</h1>"
