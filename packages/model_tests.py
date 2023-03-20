from datetime import datetime
from extensions import db
from models import *
import pytest

@pytest.fixture
def new_ingredient():
    ingredient = Ingredient(name='salt')
    db.session.add(ingredient)
    db.session.commit()
    return ingredient

@pytest.fixture
def new_menu_item(new_ingredient):
    menu_item = MenuItem(name='Chicken Curry', price=20.99, description='A delicious chicken curry', ingredients=[new_ingredient], calories=500, type='mains')
    db.session.add(menu_item)
    db.session.commit()
    return menu_item

@pytest.fixture
def new_user():
    user = User(username='test_user', password='test_password', user_type='customer', table_number=1)
    db.session.add(user)
    db.session.commit()
    return user

def test_ingredient(new_ingredient):
    assert new_ingredient.id is not None
    assert new_ingredient.name == 'salt'

def test_menu_item(new_menu_item):
    assert new_menu_item.id is not None
    assert new_menu_item.name == 'Chicken Curry'
    assert new_menu_item.price == 20.99
    assert new_menu_item.description == 'A delicious chicken curry'
    assert new_menu_item.calories == 500
    assert new_menu_item.type == 'mains'

def test_user(new_user):
    assert new_user.id is not None
    assert new_user.username == 'test_user'
    assert new_user.password == 'test_password'
    assert new_user.user_type == 'customer'
    assert new_user.table_number == 1

def test_order(new_user, new_menu_item):
    order_menu_item = OrderMenuItem(menu_item_id=new_menu_item.id, quantity=2, item_price=new_menu_item.price*2)
    order = Order(user_id=new_user.id, order_menu_items=[order_menu_item], order_total=new_menu_item.price*2)
    db.session.add(order)
    db.session.commit()
    assert order.id is not None
    assert order.user_id == new_user.id
    assert order.order_total == new_menu_item.price*2
    assert order.status == 'incomplete'
    assert order.payment_status == 'unpaid'
    assert order.delivery_status == 'waiting'
    assert order.time_placed is not None
    assert order.order_menu_items.count() == 1