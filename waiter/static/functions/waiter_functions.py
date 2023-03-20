from flask import session, url_for, redirect
from packages.models import Ingredient, MenuItem, Order, db
import functools
from sqlalchemy import text

def split_string(input_string):
    """Splits a comma separated string into a list of strings 

    Args:
        input_string (str): The comma separated string to be split

    Returns:
        List[str]: The list of the split strings
    """
    return [word.strip() for word in input_string.split(',')]

def names_to_array(ingredient_names):
    """Taks a list of ingredient names and returns an array of matching Ingredient objects from database

    Args:
        ingredient_names (List[str]): A list of ingredient names to be queried in database

    Returns:
        List: A list of Ingredient objects that matched in database with ingredient_names
    """
    ingredients = []
    # Iterate through all ingredients, if it matches in database add it to list
    for ingredient_name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient:
            ingredients.append(ingredient)
    return ingredients


def populate_menu():
    """Populated menu with data from the SQL file
    """
    # Open the SQL file and iterate through each line and execute the SQL statement
    with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
        lines = f.readlines()
        for line in lines:
            db.session.execute(text(line))
            db.session.commit()

def waiter_required(func):
    """Checks if current User is a Waiter, if not redirects User to corresponding home page

    Args:
        func (function): The function to be decorated

    Returns:
        function: The decorated function
    """    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Checks if current User is a Waiter, if not redirects User to corresponding home page if they are not

        Returns:
            function: The decorated function
        """        
        if session.get('user') != 'waiter':
            if session.get('user') == 'customer':
                return redirect(url_for('customer.home'))
            if session.get('user') == 'admin':
                return redirect(url_for('admin.home'))
            if session.get('user') == 'kitchen_staff':
                return redirect(url_for('kitchen.home'))
            else: 
                return "something went wrong"
        return func(*args, **kwargs)
    return wrapper


def add_item(name, price, description, ingredient_names, calories, type, picture):
    """_summary_

    Args:
        name (str): The name of the new MenuItem to be added
        price (float): The price of the new MenuItem to be added
        description (str): The description of the new MenuItem to be added
        ingredient_names (list): The ingredients of the new MenuItem to be added
        calories (int): The calories of the new MenuItem to be added
        type (enum): The Type of the new MenuItem to be added
        picture (str): The URL string pointing to the image of the new MenuItem to be added
    """
    # Check if each ingredient exists in the database, if not add it to the database
    for ingredient_name in ingredient_names:
        if Ingredient.query.filter_by(name=ingredient_name).first() == None:
            db.session.add(Ingredient(name = ingredient_name))
            db.session.commit()
    # Make list of ingredients        
    ingredients = names_to_array(ingredient_names)
    # Create the MenuItem and commit to database
    menu_item = MenuItem(name = name, price = price, description = description, ingredients = ingredients, calories = calories, type = type, picture=picture)
    db.session.add(menu_item)
    db.session.commit()  
    

def change_delivery(order_id, status):
    """This changes the status field of the Order in the database

    Args:
        order_id (int): The id of the Order for which status is being changed
        status (enum): The status of the Order that is being updated
    """
    # Get the Order using order_id argument and update status using status argument
    order = Order.query.get(order_id)
    order.delivery_status = status
    db.session.commit()