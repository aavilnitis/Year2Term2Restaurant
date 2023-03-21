from flask import Blueprint, render_template, request, redirect, session, jsonify, url_for, flash
from packages.models import MenuItem, Order, OrderMenuItem, User, Notification, CartItem, db
import functools
from sqlalchemy.sql import text
from .static.functions.customer_functions import populate_menu, customer_required, notification, check_tables
from .static.functions.customer_cart_functions import add_to_cart, remove_from_cart, confirm_cart

# register customer_view as a Flask Blueprint
customer = Blueprint("customer", __name__,
                     static_folder="static", template_folder="templates")


@customer.route('/')
@customer_required
def home():
    """If authenticated as Customer - Renders the home page for the customer, otherwise will redirect user to the login page

    Returns:
        str: The HTML content of the home page template
    """
    # Checks if User in session is of type Customer
    if 'user' in session:
        if session['user'] == 'customer':  # Will render home page with featured MenuItems
            menu_items = MenuItem.query.filter_by(featured=True).all()
            return render_template("home.html", menu_items=menu_items)
        else:  # If User is not a customer, render login page template
            return redirect(url_for("login.login"))
    else:
        # this is only for now:
        return render_template("home.html")


@customer.route('/featured')
@customer_required
def featured():
    """Displays featured MenuItems

    Returns:
        str: The HTML content of the menu template with featured MenuItems
    """
    # Query all featured MenuItems
    menu_items = MenuItem.query.filter_by(featured=True).all()
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


@customer.route('/filtered-menu', methods=['POST'])
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

    # Redirect customer to menu page
    return redirect(url_for("customer.menu"))


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
    cart_full = False
    if len(cart_items) > 0:
        cart_full = True
    return render_template("cart.html", cart_items=cart_items, menu_items=menu_items, cart_full=cart_full)


@customer.route('/remove_from_cart/<int:id>', methods=['POST', 'GET'])
@customer_required
def removeFromCart(id):
    """Removes MenuItem from  customers Cart 

    Args:
        id (int): The id of the MenuItem to remove from the cart

    Returns:
        flask.Response: A redirect response to the customers cart page
    """
    # Call to remove_from_cart function giving it the MenuItems id
    remove_from_cart(id)
    return redirect(url_for("customer.cart"))


@customer.route('/confirm_cart', methods=['POST', 'GET'])
@customer_required
def confirmCart():
    """Confirms the items in Cart by calling the confirm_cart function where the Order is created

    Returns:
        flask.Response: Redirects to order confirmation page or cart page if cart is empty
    """
    # Gets User.id from session
    user_id = session.get('user_id')
    # Gets CartItems associated with current customer
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if len(cart_items) > 0:
        # Function creates an Order and returns Order.id
        order_id = confirm_cart(cart_items)
        return redirect(url_for("customer.show_order", order_id=order_id))
    else:
        return redirect(url_for("customer.cart"))


@customer.route('/order/<int:order_id>')
@customer_required
def show_order(order_id):
    """Displays the details of the Order the customer has just completed

    Args:
        order_id (int): The id of the Order that is being displayed

    Returns:
        str: The HTML content for the order-confirmation page template
    """
    # Gets the Order and items that were ordered
    order = Order.query.filter_by(id=order_id).first()
    ordered_items = OrderMenuItem.query.filter_by(order_id=order.id).all()
    menu_items = MenuItem.query.all()
    return render_template("order-confirmation.html", order=order, items=ordered_items, menu_items=menu_items)


@customer.route('/orders')
@customer_required
def show_orders():
    """Displays a page to shows Order information for all orders made by current customer

    Returns:
        str: The HTML content of the order-tracking template with the users' orders 
    """
    # Gets User.id from session
    user_id = session.get('user_id')
    # Gets all orders placed by current user
    orders = Order.query.filter_by(user_id=user_id).all()
    ordered_items = {}
    # For every order it gets the items they ordered and saves it in dictioanry
    for order in orders:
        ordered_items[order.id] = OrderMenuItem.query.filter_by(
            order_id=order.id).all()
    menu_items = MenuItem.query.all()
    return render_template("order-tracking.html", orders=orders, items=ordered_items, menu_items=menu_items)


@customer.route('/table-number', methods=['GET', 'POST'])
@customer_required
def table_number():
    """Displays a form where customer selects a table number which is then updated in database

    Returns:
        flask.Response: Redirect to home page for customer
    """
    if 'user' not in session:  # Make sure user is logged in
        return "Could not add table number, are you logged in?"
    if request.method == 'POST':
        # Gets User.id from session
        user = User.query.get(session['user_id'])
        table_number = request.form['table-number']
        # Updates users table number in database
        user.table_number = table_number
        session['table_number'] = table_number
        db.session.commit()  # add table number to User table in DB
        # Creates a Notification calling the notifcation function
        notification('table')
        return redirect(url_for('home'))

    return render_template('table-number.html', free_tables=check_tables())


@customer.route('/help-needed', methods=['GET', 'POST'])
@customer_required
def help_needed():
    """Calls notfication function giving it the notification_type of help when customer wants to call waiter

    Returns:
        flask.Response: Redirect to home page for customer
    """
    notification(
        'help')  # Calls notification function to create a Notification
    return redirect(url_for('customer.home'))


@customer.route('/pay-now/<int:order_id>', methods=['GET', 'POST'])
@customer_required
def pay_now(order_id):
    """Handles payment form for an Order with the specified order_id

    Args:
        order_id (int): The id of Order for payment is being made

    Returns:
        flask.Response: If GET request is made, the payment form is rendered. If a POST request is made and payment is accepted, customer is redirected to their order-tracking page, otherwise will be redirected to a payment-error page
    """
    if request.method == 'POST':
        # Gets payment information from form
        card_number = request.form['cn']
        name_on_card = request.form['name-on-card']
        expiration_date = request.form['expiry-date']
        csv = request.form['cvv']
        # If payment is valid, update Order in database
        if len(card_number) == 16 and len(name_on_card) > 0 and len(expiration_date) == 5 and len(csv) == 3:
            order = Order.query.get(order_id)
            order.payment_status = 'paid'
            db.session.commit()
            # Successful payment means redirect back to order-tracking
            return redirect(url_for('customer.show_orders'))
        else:  # Failed payment means redirect to a payment-error page 
            return render_template('payment_error.html')
    return render_template('payment-form.html')