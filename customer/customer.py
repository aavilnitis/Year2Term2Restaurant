from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, db
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
            menu_items = MenuItem.query.filter_by(featured = True).all()
            return render_template("home.html", menu_items = menu_items)
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
@customer.route('/featured')
@customer_required
def featured():
    menu_items = MenuItem.query.filter_by(featured = True).all()
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

#Flask route for payment button
@customer.route("/pay-now")
def pay_now():
    return render_template('payment-form.html')
  
# Flask route to add an item to the cart and redirect the customer to the cart page
# This route isn't accessed manually, but instead from pressing "Add to cart" button in menu page
@customer.route('/add-to-cart/', methods=["POST"])
@customer_required
def addToCart():
    item_id = int(request.form.get("item_id"))
    if 'cart' in session:
        cart = session['cart']
        cart.append(item_id)
        session['cart'] = cart
    else: 
        create_cart()
        cart = session['cart']
        cart.append(item_id)
        session['cart'] = cart
    menu_item = MenuItem.query.get(item_id)
    flash(f"{menu_item.name} has been added to your cart", "success")
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
    user_id = session.get('user_id')
    if len(cart_ids) > 0:
        order = Order(user_id=user_id, order_menu_items=[])
        order_total = 0
        db.session.add(order)
        db.session.flush()
        for cart_id in cart_ids:
            menu_item = MenuItem.query.filter_by(id = cart_id).first()
            order_menu_item = OrderMenuItem.query.filter_by(order_id = order.id, menu_item_id = menu_item.id).first()
            if order_menu_item:
                order_menu_item.quantity += 1
                order_total += menu_item.price
            else:
                order_menu_item = OrderMenuItem(order_id=order.id, menu_item_id=menu_item.id, quantity=1)
                db.session.add(order_menu_item)
                order_total += menu_item.price
            item_total = order_menu_item.quantity * menu_item.price
            order_menu_item.item_price = item_total
            order.order_menu_items.append(order_menu_item)
        order_total = round(order_total, 2)
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
        return redirect(url_for('home'))
    return render_template('table-number.html')

@customer.route('/notify', methods=['GET','POST'])
@customer_required
def notify():
    customer_id = session.get('user_id')
    table_number = session.get('table_number')
    print(customer_id)
    if customer_id and table_number:
        notification = Notification(customer_id, table_number)
        db.session.add(notification)
        db.session.commit()
        flash('Notification sent to waiter', category='success')
        return redirect(url_for('customer.home'))
    else:
        flash('Error sending notification', category='error')
        return redirect(url_for('customer.home'))

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

@customer.route('/process_payment', methods=['POST'])
@customer_required
def process_payment():
    card_number = request.form['card_number']
    name_on_card = request.form['name_on_card']
    expiration_date = request.form['expiration_date']
    csv = request.form['csv']

    if len(card_number) == 16 and len(name_on_card) > 0 and len(expiration_date) == 5 and len(csv) == 3:
        return redirect('/order_confirmation')
    else:
        return render_template('payment_error.html')
