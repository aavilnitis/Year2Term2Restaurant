from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, db
import functools
from sqlalchemy.sql import text

# register customer_view as a Flask Blueprint
customer = Blueprint("customer", __name__, static_folder="static", template_folder="templates")


# Creates an empty array as a session directory
def create_cart():
    session['cart'] = []

# Populates the database with premade SQL inserts
def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()
            
def customer_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'customer':
            if session.get('user') == 'waiter':
                return redirect(url_for('waiter.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper

# Flask home route
@customer.route('/')
@customer_required
def home():
    if 'user' in session:
        if session['user'] == 'customer':
            return render_template("home.html")
        else:
            return redirect(url_for("login.login"))
    else:
        #this is only for now:
        return render_template("home.html")

# Flask route to view all menu items that have been added to the database
@customer.route('/menu')
@customer_required
def menu():
    if MenuItem.query.first() == None:
        populate_menu()
    menu_items = MenuItem.query.all()
    return render_template("menu.html", menu_items=menu_items)

# Flask route to view all menu items that have been added to the database
@customer.route('/filtered-menu', methods = ['POST'])
@customer_required
def filtered_menu():
    selected_categories = request.form.getlist('category')
    menu_items = []
    for category in selected_categories:
        category_items = MenuItem.query.filter_by(type=category).all()
        if category_items:
            menu_items.extend(category_items)
    return render_template("menu.html", menu_items=menu_items)

# Flask route to add an item to the cart and redirect the customer to the cart page
# This route isn't accessed manually, but instead from pressing "Add to cart" button in menu page
@customer.route('/add-to-cart/', methods=["POST"])
@customer_required
def addToCart():
    if 'cart' in session:
        cart = session['cart']
        cart.append(int(request.form.get("item_id")))
        session['cart'] = cart
        return redirect(url_for("customer.cart"))
    else: 
        create_cart()
        cart = session['cart']
        cart.append(int(request.form.get("item_id")))
        session['cart'] = cart
        return redirect(url_for("customer.cart"))

# Flask route to view all items that have been added to the cart
@customer.route('/cart')
@customer_required
def cart():
    if 'cart' in session:
        cart = session['cart']
        cart_items = []
        for id in cart:
            cart_item = MenuItem.query.filter_by(id=id).first()
            if cart_item:
                cart_items.append(cart_item)
        return render_template("cart.html", cart_items = cart_items)
    else:
        create_cart()
        return redirect(url_for("customer.cart"))

# Flask route to remove an item from the cart and redirect the customer back to the cart page
# This route isn't accessed manually, but instead from pressing "remove" button in cart
@customer.route('/remove_from_cart/<int:id>', methods=['POST', 'GET'])
@customer_required
def remove_from_cart(id):
    cart_items = session['cart']
    if id in cart_items:
        cart_items.remove(id)
    session["cart"] = cart_items
    return redirect(url_for("customer.cart"))

# Flask route to confirm an order and "send it to the restaurant"
@customer.route('/confirm_cart', methods=['POST', 'GET'])
@customer_required
def confirm_cart():
    cart_ids = session['cart']
    if len(cart_ids) > 0:
        order = Order([])
        order_total = 0
        db.session.add(order)
        db.session.flush()
        for cart_id in cart_ids:
            menu_item = MenuItem.query.filter_by(id = cart_id).first()
            order_menu_item = OrderMenuItem.query.filter_by(order_id = order.id, menu_item_id = menu_item.id).first()
            if order_menu_item:
                order_menu_item.quantity +=1
                order_total += menu_item.price
            else:
                order_menu_item = OrderMenuItem(order_id = order.id, menu_item_id = menu_item.id, quantity = 1)
                db.session.add(order_menu_item)
                order_total += menu_item.price
        order_total = round(order_total,2)
        order.order_total = order_total        
        session['cart'] = []
        db.session.commit()
        flash('Order sent to restaurant', category='success')
        return redirect(url_for("customer.show_order", order_id=order.id))
    else:
        return redirect(url_for("customer.cart"))


# Flask route to load all menu items from DB and display in a list - DEBUGGING PURPOSES
@customer.route('/view-all-items')
@customer_required
def view_all_items():
    menu_items = MenuItem.query.all()
    return render_template('view-all-items.html', items = menu_items)

# Flask route to load all orders from DB and display in a list - DEBUGGING PURPOSES
@customer.route('/view-all-orders')
@customer_required
def view_all_orders():
    orders = Order.query.all()
    menu_items = MenuItem.query.all()
    return render_template('view-all-orders.html', items = orders, menu_items = menu_items)

@customer.route('/order/<int:order_id>')
@customer_required
def show_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    ordered_items = OrderMenuItem.query.filter_by(order_id=order.id).all()
    menu_items = MenuItem.query.all()
    return render_template("order-confirmation.html", order = order, items=ordered_items, menu_items = menu_items)


@customer.route('/notify', methods=['POST'])
@customer_required
def notify():
    customer_id = session.get('customer_id')
    table_number = session.get('table_number')
    if customer_id and table_number:
        db.session.execute(
            text("INSERT INTO notifications (customer_id, table_number) VALUES (:customer_id, :table_number)"),
            {"customer_id": customer_id, "table_number": table_number}
        )
        db.session.commit()
        flash('Notification sent to waiter', category='success')
        return redirect(url_for('customer.home'))
    else:
        flash('Error sending notification', category='error')
        return redirect(url_for('customer.home'))