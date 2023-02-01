--Insert ingredients into ingredients table here
INSERT INTO ingredients (name) VALUES ('cheese');

--Insert menu_items into menu_items here
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Coca-Cola', 2.99, 'Classic soda made with real sugar.', 40, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Iced Tea', 2.49, 'Refreshing iced tea made with real tea leaves.', 5, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Lemonade', 2.99, 'Tart and sweet homemade lemonade.', 21, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Toilet Water', 50000.99, 'Its better than you think', 102, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Cheeseburger', 8.99, 'Juicy beef patty topped with melted cheese and served on a sesame seed bun.', 480, 'food');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('BLT', 6.99, 'Crispy bacon, lettuce, and tomato served on white toast.', 720, 'food');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Chalk', 777.99, 'Its just chalk.', 2199, 'food');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Worlds Largest Pepperoni Pizza', 99999.99, 'Our magnum opus, an eighty inch pizza. You wont get it through your door!', 10999, 'food');

--Associate the ingredients to menu item here using id
--Example Insert here add Cheese to Cheeseburger using their respective ID's
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 1);