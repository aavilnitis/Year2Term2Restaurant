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
    cart_item = CartItem.query.filter_by(user_id=user_id, menu_item_id=item_id).first()
    
    if cart_item: # If CartItem exists, update its quantity and item_price
        cart_item.quantity += quantity
        cart_item.item_price += (quantity * menu_item.price)
    else: # If it doesn't exists, create a new CartItem using the item_id and quantity parameters
        cart_item = CartItem(user_id=user_id, menu_item_id=item_id, quantity=quantity, item_price=(quantity * menu_item.price))
        db.session.add(cart_item)
    
    db.session.commit() # Commit changes to the database
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
    cart_item = CartItem.query.filter_by(user_id=user_id, menu_item_id=id).first()

    # If quantity of existing CartItem is greater than 1, update its quantity and item_price
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.item_price -= menu_item.price
    else: # If quantity is 1, delete the CartItem from database
        db.session.delete(cart_item)

    # Commit changes to the database    
    db.session.commit()
    flash(f"1 x{menu_item.name} has been removed from your cart", "success")


def confirm_cart(cart_items):
    user_id = session.get('user_id')
    table_number = session.get('table_number')
    order = Order(user_id=user_id, order_menu_items=[])
    order_total = 0
    db.session.add(order)
    db.session.flush()
    for cart_item in cart_items:
        menu_item = MenuItem.query.filter_by(id = cart_item.menu_item_id).first()
        order_menu_item = OrderMenuItem(order_id=order.id, menu_item_id=menu_item.id, quantity=cart_item.quantity, item_price = cart_item.item_price)
        order_total += order_menu_item.item_price
        db.session.add(order_menu_item)
        order.order_menu_items.append(order_menu_item)
    order_total = round(order_total, 2)
    order.order_total = order_total   

    for cart_item in cart_items:
        db.session.delete(cart_item)     
        
    notif = Notification(user_id, table_number, 'new-order')
    db.session.add(notif)
    db.session.commit()
    flash('Order sent to restaurant', category='success')
    return order.id