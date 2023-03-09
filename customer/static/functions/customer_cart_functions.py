from flask import session, request, flash
from packages.models import MenuItem, Order, OrderMenuItem, CartItem, db

def create_cart():
    session['cart'] = []

def add_to_cart(item_id):
    user_id = session.get('user_id')
    item_id = int(request.form.get("item_id"))
    menu_item = MenuItem.query.get(item_id)
    cart_item = CartItem.query.filter_by(menu_item_id=item_id).first()
    
    if cart_item:
        cart_item.quantity += 1
        cart_item.item_price += menu_item.price
    else:
        cart_item = CartItem(user_id=user_id,menu_item_id=item_id, quantity=1, item_price=menu_item.price)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f"{menu_item.name} has been added to your cart", "success")


def remove_from_cart(id):
    cart_items = session['cart']
    if id in cart_items:
        cart_items.remove(id)
    session["cart"] = cart_items


def confirm_cart(cart_ids):
    user_id = session.get('user_id')
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
    return order.id