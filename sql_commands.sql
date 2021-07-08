-- SQLite
SELECT * FROM recipes;
SELECT * FROM users;
SELECT * FROM users_recipes;
SELECT * FROM recipes_ingredients;
SELECT * FROM ingredients;
SELECT * FROM users_shoplists;
SELECT * FROM shoplist_ingredients;
SELECT * FROM shoplists;


DELETE FROM ingredients;
DELETE FROM recipes;
DELETE FROM users_recipes;
DELETE FROM users_shoplists;
DELETE FROM shoplist_ingredients;
DELETE FROM recipes_ingredients;
DELETE FROM users;
DELETE FROM shoplists;

-- DROP TABLE recipes;
-- DROP TABLE users;
-- DROP TABLE ingredients;
-- DROP TABLE users_recipes;
-- DROP TABLE recipes_ingredients;
DROP TABLE users_shoplists;