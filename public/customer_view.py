from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for
from public.models import MenuItem, Order, db
from sqlalchemy.sql import text

customer_view = Blueprint('customer_view', __name__)

def create_cart():
    session['cart'] = []

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


@customer_view.route('/add-to-cart/', methods=["POST"])
def addToCart():
    if 'cart' in session:
        cart = session['cart']
        cart.append(int(request.form.get("item_id")))
        session['cart'] = cart
        return redirect(url_for("customer_view.cart"))
    else: 
        create_cart()
        return redirect(url_for("customer_view.addToCart"))


@customer_view.route('/cart')
def cart():
    cart = session['cart']
    cart_items = []
    for id in cart:
        cart_item = MenuItem.query.filter_by(id=id).first()
        if cart_item:
            cart_items.append(cart_item)

    
    return render_template("cart.html", cart_items = cart_items)


@customer_view.route('/view-all-items')
def view_all_items():
    menu_items = MenuItem.query.all()
    return render_template('view-all-items.html', menu_items = menu_items)


@customer_view.route('/view-all-orders')
def view_all_orders():
    return render_template('base.html')