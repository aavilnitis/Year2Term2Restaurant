from . import db
from flask_sqlalchemy import SQLAlchemy

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(300))
    type = db.Column(db.Enum('food', 'drink', name='menuItem_type'), nullable = False)

    def __init__(self, name, price, description, type):
        self.name = name
        self.price = price
        self.description = description
        self.type = type

#association table
order_menu_item = db.Table("order_menu_item",
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), primary_key=True),
    db.Column("menu_item_id", db.Integer, db.ForeignKey("menu_items.id"), primary_key=True)
)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True)
    menu_items_list = db.relationship("MenuItem", secondary = order_menu_item, back_populates="orders")
    order_total = db.Column(db.Float, nullable = False, default = 0)
    status = db.Column(db.Enum('complete', 'incomplete', name='order_status'), nullable = False, defualt = 'incomplete')
    
    def __init__(self, menu_items_list, order_total = 0, status = 'incomplete'):
        self.menu_items_list = menu_items_list
        self.order_total = order_total
        self.status = status
   