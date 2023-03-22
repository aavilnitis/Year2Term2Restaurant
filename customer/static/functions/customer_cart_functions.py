from flask import session, request, flash
from packages.models import MenuItem, Order, Notification, OrderMenuItem, CartItem, db


def add_to_cart(item_id, quantity):
    """Creates a CartItem using parameters given or updates quantity and item_price of existing CartItem

    Args:
        item_id (int): The id of the MenuItem being added to cart from the menu
        quantity (int): The quantity of MenuItems being added to cart from the menu
    """
    # Get User.id saved in session
    user_id = session.get('user_id')

    # Retrieve the MenuItem using id parameter and the corresponding CartItem from database
    menu_item = MenuItem.query.get(item_id)
    cart_item = CartItem.query.filter_by(
        user_id=user_id, menu_item_id=item_id).first()

    if cart_item:  # If CartItem exists, update its quantity and item_price
        cart_item.quantity += quantity
        cart_item.item_price += (quantity * menu_item.price)
    else:  # If it doesn't exists, create a new CartItem using the item_id and quantity parameters
        cart_item = CartItem(user_id=user_id, menu_item_id=item_id,
                             quantity=quantity, item_price=(quantity * menu_item.price))
        db.session.add(cart_item)
    
    cart_amount = session['cart-amount'] + quantity
    session['cart-amount'] = cart_amount
    db.session.commit()
    flash(f"{menu_item.name} has been added to your cart", "success")


def remove_from_cart(id):
    """Deletes a CartItem using parameter given or updates quantity and item_price of existing CartItem

    Args:
        id (int): The id of the MenuItem being removed from the cart
    """
    # Get User.id saved in session
    user_id = session.get('user_id')

    # Retrieve the MenuItem using id parameter and the corresponding CartItem from database
    menu_item = MenuItem.query.get(id)
    cart_item = CartItem.query.filter_by(
        user_id=user_id, menu_item_id=id).first()

    # If quantity of existing CartItem is greater than 1, update its quantity and item_price
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.item_price -= menu_item.price
    else:  # If quantity is 1, delete the CartItem from database
        db.session.delete(cart_item)
    
    cart_amount = session['cart-amount'] - 1
    session['cart-amount'] = cart_amount
    db.session.commit()
    flash(f"1 x{menu_item.name} has been removed from your cart", "success")


def confirm_cart(cart_items):
    """Converts CartItems for current user to OrderMenuItems and adding them to a Order 

    Args:
        cart_items (list): A list of CartItem objects to be convered to OrderMenuItems

    Returns:
        int: The id of the created Order
    """

    # Get User.id saved in session
    user_id = session.get('user_id')

    # Get User.table_number saved in session
    table_number = session.get('table_number')

    # Create a empty Order and a order_total of 0
    order = Order(user_id=user_id, order_menu_items=[])
    order_total = 0

    # Add Order to database and flush to get the Order.id
    db.session.add(order)
    db.session.flush()

    # Iterate through list of CartItems and create OrderMenuItem using information from the CartItem and corresponding MenuItem
    for cart_item in cart_items:
        menu_item = MenuItem.query.filter_by(id=cart_item.menu_item_id).first()
        order_menu_item = OrderMenuItem(order_id=order.id, menu_item_id=menu_item.id,
                                        quantity=cart_item.quantity, item_price=cart_item.item_price)

        # Update order_total after OrderMenuItem has been created
        order_total += order_menu_item.item_price
        db.session.add(order_menu_item)

        # Add the OrderMenuItem to the list of order_menu_items of Order
        order.order_menu_items.append(order_menu_item)

    order_total = round(order_total, 2)

    # Update Order.order_total
    order.order_total = order_total

    # Iterate through list of CartItems and delete them as they are no longer needed
    for cart_item in cart_items:
        db.session.delete(cart_item)

    # Create Notification to let staff know of the new order that has been created
    notif = Notification(user_id, table_number, 'new-order')
    db.session.add(notif)

    # Commit changes to the database
    db.session.commit()
    flash('Order sent to restaurant', category='success')
    session['cart-amount'] = 0
    return order.id