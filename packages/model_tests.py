from datetime import datetime
from packages.extensions import db
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