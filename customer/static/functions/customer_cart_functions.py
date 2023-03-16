from flask import session, request, flash
from packages.models import MenuItem, Order, Notification, OrderMenuItem, CartItem, db

def add_to_cart(item_id, quantity):
    user_id = session.get('user_id')
    menu_item = MenuItem.query.get(item_id)
    cart_item = CartItem.query.filter_by(user_id=user_id, menu_item_id=item_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
        cart_item.item_price += (quantity * menu_item.price)
    else:
        cart_item = CartItem(user_id=user_id, menu_item_id=item_id, quantity=quantity, item_price=(quantity * menu_item.price))
        db.session.add(cart_item)
    
    cart_amount = session['cart-amount'] + quantity
    session['cart-amount'] = cart_amount
    db.session.commit()
    flash(f"{menu_item.name} has been added to your cart", "success")


def remove_from_cart(id):
    user_id = session.get('user_id')
    menu_item = MenuItem.query.get(id)
    cart_item = CartItem.query.filter_by(user_id=user_id, menu_item_id=id).first()

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.item_price -= menu_item.price
    else:
        db.session.delete(cart_item)
    
    cart_amount = session['cart-amount'] - 1
    session['cart-amount'] = cart_amount
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