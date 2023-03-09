from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
import functools
from sqlalchemy.sql import text
from .static.functions.customer_functions import populate_menu, customer_required, notification, check_tables
from .static.functions.customer_cart_functions import create_cart, add_to_cart, remove_from_cart, confirm_cart

# register customer_view as a Flask Blueprint
customer = Blueprint("customer", __name__, static_folder="static", template_folder="templates")

# HOME AND FEATURED

# Flask home route
@customer.route('/')
@customer_required
def home():
    if 'user' in session:
        if session['user'] == 'customer':
            menu_items = MenuItem.query.filter_by(featured = True).all()
            return render_template("home.html", menu_items = menu_items)
        else:
            return redirect(url_for("login.login"))
    else:
        #this is only for now:
        return render_template("home.html")
    
# Flask route to view all menu items that have been added to the database
@customer.route('/featured')
@customer_required
def featured():
    menu_items = MenuItem.query.filter_by(featured = True).all()
    return render_template("menu.html", menu_items=menu_items)



# MENU AND FILTERED MENU

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



# CART FUNCTIONS AND ROUTES

# Flask route to add an item to the cart and redirect the customer to the cart page
# This route isn't accessed manually, but instead from pressing "Add to cart" button in menu page
@customer.route('/add-to-cart/', methods=["POST"])
@customer_required
def addToCart():
    item_id = int(request.form.get("item_id"))
    add_to_cart(item_id)
    return redirect(url_for("customer.menu"))

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
def removeFromCart(id):
    remove_from_cart(id)
    return redirect(url_for("customer.cart"))

# Flask route to confirm an order and "send it to the restaurant"
@customer.route('/confirm_cart', methods=['POST', 'GET'])
@customer_required
def confirmCart():
    cart_ids = session['cart']
    if len(cart_ids) > 0:
        order_id = confirm_cart(cart_ids)
        return redirect(url_for("customer.show_order", order_id=order_id))
    else:
        return redirect(url_for("customer.cart"))



# ORDER FUNCTIONS AND ROUTES

@customer.route('/order/<int:order_id>')
@customer_required
def show_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    ordered_items = OrderMenuItem.query.filter_by(order_id=order.id).all()
    menu_items = MenuItem.query.all()
    return render_template("order-confirmation.html", order = order, items=ordered_items, menu_items = menu_items)

@customer.route('/orders')
@customer_required
def show_orders():
    user_id = session.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).all()
    ordered_items = {}
    for order in orders:
        ordered_items[order.id] = OrderMenuItem.query.filter_by(order_id=order.id).all()
    menu_items = MenuItem.query.all()
    return render_template("order-tracking.html", orders=orders, items=ordered_items, menu_items=menu_items)



# TABLES AND NOTIFICATIONS

@customer.route('/table-number', methods=['GET', 'POST'])
@customer_required
def table_number():
    if 'user' not in session: # make sure user is logged in
        return "Could not add table number, are you logged in?"
    if request.method == 'POST':
        
        user = User.query.get(session['user_id'])
        table_number = request.form['table-number']
        user.table_number = table_number
        session['table_number'] = table_number
        db.session.commit() #add table number to User table in DB
        notification('table')
        return redirect(url_for('home'))
    
    return render_template('table-number.html', free_tables = check_tables())



@customer.route('/help-needed', methods=['GET','POST'])
@customer_required
def help_needed():
    notification('help')
    return redirect(url_for('customer.home'))




# PAYMENT FORM AND PROCESSING

#Flask route for payment button
@customer.route('/pay-now/<int:order_id>', methods=['GET','POST'])
@customer_required
def pay_now(order_id):
    if request.method == 'POST':
        card_number = request.form['cn']
        name_on_card = request.form['name-on-card']
        expiration_date = request.form['expiry-date']
        csv = request.form['cvv']
        if len(card_number) == 16 and len(name_on_card) > 0 and len(expiration_date) == 5 and len(csv) == 3:
            order = Order.query.get(order_id)
            order.payment_status = 'paid'
            db.session.commit()
            return redirect(url_for('customer.show_orders'))
        else:
            return render_template('payment_error.html')
    return render_template('payment-form.html')


