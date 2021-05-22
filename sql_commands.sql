-- SQLite
SELECT * FROM recipes;
SELECT * FROM users;
SELECT * FROM users_recipes;
SELECT * FROM recipes_ingredients;
SELECT * FROM ingredients;


DELETE FROM ingredients;
DELETE FROM recipes;
DELETE FROM users_recipes;
DELETE FROM recipes_ingredients;
DELETE FROM users;

DROP TABLE recipes;
DROP TABLE users;
DROP TABLE ingredients;
DROP TABLE users_recipes;
DROP TABLE recipes_ingredients;