--INSERTING INGREDIENTS
--coca cola
INSERT INTO ingredients (name) VALUES ('carbonated water');
INSERT INTO ingredients (name) VALUES ('sugar');
INSERT INTO ingredients (name) VALUES ('Caffeine');
--iced tea
INSERT INTO ingredients (name) VALUES ('tea bags');
INSERT INTO ingredients (name) VALUES ('sugar');
INSERT INTO ingredients (name) VALUES ('lemons sliced');
--lemonade
INSERT INTO ingredients (name) VALUES ('sugar');
INSERT INTO ingredients (name) VALUES ('water');
INSERT INTO ingredients (name) VALUES ('lemon juice');
--toilet water
INSERT INTO ingredients (name) VALUES ('vodka');
INSERT INTO ingredients (name) VALUES ('triple sec');
INSERT INTO ingredients (name) VALUES ('lemon lime soda');
--cheese burger
INSERT INTO ingredients (name) VALUES ('cheese');
INSERT INTO ingredients (name) VALUES ('lettuce');
INSERT INTO ingredients (name) VALUES ('red onion');
--BLT
INSERT INTO ingredients (name) VALUES ('Bacon');
INSERT INTO ingredients (name) VALUES ('lettuce');
INSERT INTO ingredients (name) VALUES ('tomato');
--chalk
INSERT INTO ingredients (name) VALUES ('sugar');
INSERT INTO ingredients (name) VALUES ('cocoa powder');
INSERT INTO ingredients (name) VALUES ('corn syrup');
--pepperoni pizza
INSERT INTO ingredients (name) VALUES ('online');
INSERT INTO ingredients (name) VALUES ('pepperoni');
INSERT INTO ingredients (name) VALUES ('garlic');
--INSERTING MENU ITEMS
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Coca-Cola', 2.99, 'Classic soda made with real sugar.', 40, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Iced Tea', 2.49, 'Refreshing iced tea made with real tea leaves.', 5, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Lemonade', 2.99, 'Tart and sweet homemade lemonade.', 21, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Toilet Water', 50000.99, 'Its better than you think', 102, 'drink');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Cheeseburger', 8.99, 'Juicy beef patty topped with melted cheese and served on a sesame seed bun.', 480, 'food');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('BLT', 6.99, 'Crispy bacon, lettuce, and tomato served on white toast.', 720, 'food');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Chalk', 777.99, 'Its just chalk.', 2199, 'food');
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Worlds Largest Pepperoni Pizza', 99999.99, 'Our magnum opus, an eighty inch pizza. You wont get it through your door!', 10999, 'food');
--ASSOCIATING ingridients to menu items using the ID
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (1, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (1, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (1, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (2, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (2, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (2, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (3, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (3, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (3, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (4, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (4, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (4, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (6, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (6, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (6, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (7, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (7, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (7, 3);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (8, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (8, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (8, 3);