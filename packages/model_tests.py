from datetime import datetime
from extensions import db
from models import Ingredient, MenuItem, Order, OrderMenuItem, CartItem, User

def test_ingredient():
    ingredient = Ingredient(name="onion")
    assert ingredient.name == "onion"

def test_menu_item():
    ingredient1 = Ingredient(name="onion")
    ingredient2 = Ingredient(name="cheese")
    menu_item = MenuItem(name="pizza", price=12.99, description="Yummy Pizza", 
                         ingredients=[ingredient1, ingredient2], calories=500, 
                         type="mains", picture="pizza.jpg")
    assert menu_item.name == "pizza"
    assert menu_item.price == 12.99
    assert menu_item.description == "Yummy Pizza"
    assert menu_item.calories == 500
    assert menu_item.type == "mains"
    assert menu_item.picture == "pizza.jpg"

def test_order():
    user = User(username="testuser", password="password", user_type="customer")
    order_menu_item = OrderMenuItem(menu_item_id=1, quantity=2, item_price=25.99)
    order = Order(user_id=user.id, order_menu_items=[order_menu_item], order_total=51.98, 
                  status="confirmed", payment_status="paid", delivery_status="delivered", 
                  time_placed=datetime.utcnow())
    assert order.user_id == user.id
    assert order.order_total == 51.98
    assert order.status == "confirmed"
    assert order.payment_status == "paid"
    assert order.delivery_status == "delivered"
    assert order.time_placed is not None

def test_order_menu_item():
    order_menu_item = OrderMenuItem(menu_item_id=1, quantity=2, item_price=25.99)
    assert order_menu_item.menu_item_id == 1
    assert order_menu_item.quantity == 2
    assert order_menu_item.item_price == 25.99