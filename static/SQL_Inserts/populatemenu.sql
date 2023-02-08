--INSERTING INGREDIENTS FOR EACH MENUITEM
--coca cola
INSERT INTO ingredients (name) VALUES ('carbonated water');--1
INSERT INTO ingredients (name) VALUES ('sugar');--2
INSERT INTO ingredients (name) VALUES ('Caffeine');--3

--iced tea
INSERT INTO ingredients (name) VALUES ('tea bags');--4
--INSERT INTO ingredients (name) VALUES ('sugar');
INSERT INTO ingredients (name) VALUES ('lemons sliced');--5

--lemonade
--2
INSERT INTO ingredients (name) VALUES ('water');--6
INSERT INTO ingredients (name) VALUES ('lemon juice');--7

--toilet water
INSERT INTO ingredients (name) VALUES ('vodka');--8
INSERT INTO ingredients (name) VALUES ('triple sec');--9
INSERT INTO ingredients (name) VALUES ('lemon lime soda');--10

--cheese burger
INSERT INTO ingredients (name) VALUES ('cheese');--11
INSERT INTO ingredients (name) VALUES ('lettuce');--12
INSERT INTO ingredients (name) VALUES ('red onion');--13

--BLT
INSERT INTO ingredients (name) VALUES ('Bacon');--14
--12
INSERT INTO ingredients (name) VALUES ('tomato');--15

--chalk
--2
INSERT INTO ingredients (name) VALUES ('cocoa powder');--16
INSERT INTO ingredients (name) VALUES ('corn syrup');--17

--pepperoni pizza
--11
INSERT INTO ingredients (name) VALUES ('pepperoni');--18
INSERT INTO ingredients (name) VALUES ('garlic');--19

--Inserting CocaCola and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Coca-Cola', 2.99, 'Classic soda made with real sugar.', 40, 'drink');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (1, 1);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (1, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (1, 3);

--Inserting Iced tea and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Iced Tea', 2.49, 'Refreshing iced tea made with real tea leaves.', 5, 'drink');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (2, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (2, 4);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (2, 5);

--Inserting Lemonade and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Lemonade', 2.99, 'Tart and sweet homemade lemonade.', 21, 'drink');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (3, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (3, 6);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (3, 7);

--Inserting Toilet Water and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Toilet Water', 50000.99, 'Its better than you think', 102, 'drink');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (4, 8);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (4, 9);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (4, 10);

--Inserting Cheeseburger and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Cheeseburger', 8.99, 'Juicy beef patty topped with melted cheese and served on a sesame seed bun.', 480, 'food');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 11);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 12);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (5, 13);

--Inserting BLT and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('BLT', 6.99, 'Crispy bacon, lettuce, and tomato served on white toast.', 720, 'food');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (6, 14);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (6, 12);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (6, 15);

--Inserting Chalk and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Chalk', 777.99, 'Its just chalk.', 2199, 'food');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (7, 2);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (7, 16);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (7, 17);

--Inserting Pepperoni pizza and Ingredients
INSERT INTO menu_items (name, price, description, calories, type) VALUES ('Worlds Largest Pepperoni Pizza', 99999.99, 'Our magnum opus, an eighty inch pizza. You wont get it through your door!', 10999, 'food');
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (8, 11);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (8, 18);
INSERT INTO menu_item_ingredient (menu_item_id, ingredient_id) VALUES (8, 19);