from . import db
from flask_sqlalchemy import SQLAlchemy

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(300))
    type = db.Column(db.Enum('food', 'drink', name='menuItem_type'), nullable = False)

    def __init__(self, name, price, description, type):
        self.name = name
        self.price = price
        self.description = description
        self.type = type

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_total = db.Column(db.Float, nullable = False)
    status = db.Column(db.Enum('complete', 'incomplete', name='order_status'), nullable = False)
    
    def __init__(self, order_total, status):
        self.order_total = order_total
        self.status = status
   