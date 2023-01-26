from flask import Blueprint,render_template
from public.models import MenuItem, db

customer_view = Blueprint('customer_view', __name__)


@customer_view.route('/')
def home():
    return render_template("home.html")

@customer_view.route('/menu')
def menu():
    menu_items = MenuItem.query.all()
    return render_template("menu.html", menu_items = menu_items)

@customer_view.route('/cart')
def cart():
    return render_template('cart.html')

@customer_view.route('/view-all-items')
def view_all_items():
    return render_template('view-all-items.html')

@customer_view.route('/view-all-orders')
def view_all_orders():
    return render_template('base.html')