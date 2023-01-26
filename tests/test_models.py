import os
import unittest
from sqlalchemy.sql import text
from public import create_app, db
from public import models

class TestModels(unittest.TestCase):
    def setUp(self):
        #setting up the database to test
        self.app = create_app()
        self.app.config['Testing'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        with self.app.app_context():
            #creating the tables in the database
            self.db = db
            self.db.create_all()
            #opening sql file and executing each line
            with open("static/SQL_Inserts/populatemenu.sql", "r") as f:
                lines = f.readlines()
                for line in lines:
                    self.db.session.execute(text(line))
                self.db.session.commit()
        
    def test_menu_item_creation(self):
        with self.app.app_context():
            #creating a MenuItem model
            item = models.MenuItem(name = 'Wings', price = 5.99, description = 'the best bbq wings you can have', type = 'food')
            #adding it to table in database.db
            self.db.session.add(item)
            self.db.session.commit()
            #finder the first result with name of Wings
            result = models.MenuItem.query.filter_by(name='Wings').first()
            #checking if they have the same price
            self.assertEqual(result.price, 5.99) 

    def test_sql(self):
        with self.app.app_context():
            #finding the first menuitem with name Cheeseburger
            sql_result = models.MenuItem.query.filter_by(name = 'Cheeseburger').first()
            #checking if they have the same price
            self.assertEqual(sql_result.price, 8.99)                                                           



if __name__ == '__main__':
    unittest.main           