from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, CartItem, db
import functools
from sqlalchemy.sql import text
from .static.functions.customer_functions import populate_menu, customer_required, notification, check_tables
from .static.functions.customer_cart_functions import add_to_cart, remove_from_cart, confirm_cart

# register customer_view as a Flask Blueprint
customer = Blueprint("customer", __name__, static_folder="static", template_folder="templates")

@customer.route('/')
@customer_required
def home():
    """If authenticated as Customer - Renders the home page for the customer, otherwise will redirect user to the login page

    Returns:
        str: The HTML content of the home page template
    """
    # Checks if User in session is of type Customer
    if 'user' in session:
        if session['user'] == 'customer': # Will render home page with featured MenuItems
            menu_items = MenuItem.query.filter_by(featured = True).all()
            return render_template("home.html", menu_items = menu_items)
        else: # If User is not a customer, render login page template
            return redirect(url_for("login.login"))
    else:
        #this is only for now:
        return render_template("home.html")
    

@customer.route('/featured')
@customer_required
def featured():
    """Displays featured MenuItems

    Returns:
        str: The HTML content of the menu template with featured MenuItems
    """
    # Query all featured MenuItems
    menu_items = MenuItem.query.filter_by(featured = True).all()
    return render_template("menu.html", menu_items=menu_items)


@customer.route('/menu')
@customer_required
def menu():
    """Checks if a MenuItem exists, if not it will call the populate_menu function to update menu data

    Returns:
        str: The HTML content for the menu page template with all MenuItems
    """
    # Calls populate_menu if there are no MenuItems
    if MenuItem.query.first() == None:
        populate_menu()
    # Query all MenuItems and render menu template
    menu_items = MenuItem.query.all()
    return render_template("menu.html", menu_items=menu_items)


@customer.route('/filtered-menu', methods = ['POST'])
@customer_required
def filtered_menu():
    """Renders menu template with MenuItems based on the selected categories by Customer

    Returns:
        str: The HTML content of menu page template with filetered MenuItems
    """
    # Retrieve selected categories from POST request
    selected_categories = request.form.getlist('category')

    # Loop through selected_categories and add MenuItem of that category to list menu_items
    menu_items = []
    for category in selected_categories:
        category_items = MenuItem.query.filter_by(type=category).all()
        # If there is a MenuItem of that category, add it to menu_items list
        if category_items: 
            menu_items.extend(category_items)
    return render_template("menu.html", menu_items=menu_items)


@customer.route('/add-to-cart/', methods=["POST"])
@customer_required
def addToCart():
    """Adds selected MenuItems to the cart by calling a add_to_cart method

    Returns:
        flask.Response: A Flask redirect response to the customer menu page
    """
    # Retrieves MenuItem's id and quantity from POST request form
    item_id = int(request.form.get("item_id"))
    quantity = int(request.form.get("quantity"))

    # Calls add_to_cart functions with the retrieved item_id and quantity
    add_to_cart(item_id, quantity)

    #Redirect customer to menu page
    return redirect(url_for("customer.menu"))

# Flask route to view all items that have been added to the cart
@customer.route('/cart')
@customer_required
def cart():
    """Displays the items in cart using current users id stored in session

    Returns:
        str: The HTML content of the cart page template
    """
    # Gets the User.id stored in session and associated CartItems
    user_id = session.get('user_id')
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    
    # Gets all Menuitems to help display item details in the cart
    menu_items = MenuItem.query.all()
    return render_template("cart.html", cart_items = cart_items, menu_items = menu_items)

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
    user_id = session.get('user_id')
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if len(cart_items) > 0:
        order_id = confirm_cart(cart_items)
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


