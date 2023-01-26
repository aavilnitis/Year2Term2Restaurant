from flask import Blueprint,render_template
from public.models import MenuItem, db
from sqlalchemy.sql import text

customer_view = Blueprint('customer_view', __name__)

def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
                lines = f.readlines()
                for line in lines:
                    db.session.execute(text(line))
                db.session.commit()


@customer_view.route('/')
def home():
    return render_template("home.html")

@customer_view.route('/menu')
def menu():
    if MenuItem.query.filter_by(name = "Cheeseburger").first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template("menu.html", menu_items=menu_items)

@customer_view.route('/cart')
def cart():
    return render_template('cart.html')

@customer_view.route('/view-all-items')
def view_all_items():
    menu_items = MenuItem.query.all()
    return render_template('view-all-items.html', menu_items = menu_items)

@customer_view.route('/view-all-orders')
def view_all_orders():
    return render_template('base.html')