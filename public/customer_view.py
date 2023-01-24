from flask import Blueprint,render_template

customer_view = Blueprint('customer_view', __name__)


@customer_view.route('/')
def home():
    return render_template("home.html")
