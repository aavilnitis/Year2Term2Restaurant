from flask import session, url_for, redirect
from packages.models import Ingredient, MenuItem, db
import functools
from sqlalchemy import text

def split_string(input_string):
    return [word.strip() for word in input_string.split(',')]

def names_to_array(ingredient_names):
    ingredients = []
    for ingredient_name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient:
            ingredients.append(ingredient)
    return ingredients

# Populates the database with premade SQL inserts
def populate_menu():
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()

def waiter_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') != 'waiter':
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper

def add_item(name, price, description, ingredient_names, calories, type, picture):
    for ingredient_name in ingredient_names:
        if Ingredient.query.filter_by(name=ingredient_name).first() == None:
            db.session.add(Ingredient(name = ingredient_name))
            db.session.commit()
    ingredients = names_to_array(ingredient_names)
    menu_item = MenuItem(name = name, price = price, description = description, ingredients = ingredients, calories = calories, type = type, picture=picture)
    db.session.add(menu_item)
    db.session.commit()  