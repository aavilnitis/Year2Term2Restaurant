from datetime import datetime
from packages.extensions import db

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)

    def __init__(self, name):
        self.name = name

menu_item_ingredient = db.Table("menu_item_ingredient",
    db.Column("menu_item_id", db.Integer, db.ForeignKey("menu_items.id"), primary_key=True),
    db.Column("ingredient_id", db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)
) 

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300))
    ingredients = db.relationship("Ingredient", secondary=menu_item_ingredient, lazy="dynamic")
    calories = db.Column(db.Integer)
    type = db.Column(db.Enum('starters', 'mains', 'sides', 'desserts', 'drinks', name='MenuItem_type'), nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    featured = db.Column(db.Boolean, default=False, nullable=True)

    def __init__(self, name, price, description, ingredients, calories, type, picture=None):
        self.name = name
        self.price = price
        self.description = description
        self.ingredients = ingredients
        self.calories = calories
        self.type = type
        self.picture = picture


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_menu_items = db.relationship("OrderMenuItem", backref = "order", lazy = "dynamic")
    order_total = db.Column(db.Float, nullable = False, default = 0)
    status = db.Column(db.Enum('complete', 'incomplete', name='order_status'), nullable = False, default = 'incomplete')
    payment_status = db.Column(db.Enum('paid', 'unpaid', name='payment_status'), nullable = False, default = 'unpaid')
    delivery_status = db.Column(db.Enum('waiting', 'preparing', 'ready', 'on the way', 'delivered', name='delivery_status'), nullable = False, default = 'waiting')
    time_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    def __init__(self, user_id, order_menu_items, order_total = 0, status = 'incomplete', payment_status = 'unpaid', delivery_status = 'waiting', time_placed = None):
        self.user_id = user_id
        self.order_menu_items = order_menu_items
        self.order_total = order_total
        self.status = status
        self.payment_status = payment_status
        self.delivery_status = delivery_status
        if time_placed is not None:
            self.time_placed = time_placed
        else:
            self.time_placed = datetime.utcnow()

class OrderMenuItem(db.Model):
    __tablename__ = "order_menu_item"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable = False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable = False)
    quantity = db.Column(db.Integer, nullable = False, default = 1)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(1000), nullable = False)
    user_type = db.Column(db.Enum('customer', 'waiter', 'kitchen_staff', name='user_type'), nullable = False)
    table_number = db.Column(db.Integer)

    def __init__(self, username, password, user_type, table_number = None):
        self.username = username
        self.password = password
        self.user_type = user_type
        if user_type == 'customer':
            self.table_number = table_number
        else:
            self.table_number = None

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    table_number = db.Column(db.Integer, db.ForeignKey('users.table_number'))
    status = db.Column(db.Enum('helped', 'not_helped', name = 'notification_status'), nullable=False, default='not_helped')

    def __init__(self, user_id, table_number):
        self.user_id = user_id
        self.table_number = table_number
        #if User.query.filter_by(id = user_id, user_type = 'customer').first() and table_number is not None:
        #    self.user_id = user_id
        #    self.table_number = table_number
        #else:
        #    raise ValueError("It seems you have forgotten to enter table number or you are not logged in as a customer.")