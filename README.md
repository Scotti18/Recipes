
# Your personal E-Coobook

#### Video Demo: <URL Here>
#### Description:

# My project is a flask based web application replacing your traditional, heavy cookbooks
# with a digital version! You have all your favourite recipes in one place plus extra
# functionalities like creating  personalized shopping lists.

#### Structure of the Application

# The web application uses flask as a framework and the routes are split up using blureprints,
# to keep the code organized and have reusuable components (like registration/login).
# Currently there are only two blueprints, one when being logged in and one for when being logged out (Homepage + Login/Registration).


# In the auth (authentication) blueprint you can find cover.html, login.html, and register.html. 
# When you first visit the website you land on cover.html and get information about the functionality in a slideshow (CSS)
# You can then regsiter and log in to get to the main application.
# When logging in, you start a flask session and are then able to access (secured with the @login_required decorator) the views blueprint.


# You start of at index.html where you can add recipes to your coobkook in a variety of ways.
# Firstly, you can search google recipes using the google search api (api key and cx necessary) or you can
# paste in any link from the web that contains a recipe.
# For either of these two ways, I used the scrape_me function from recipe_scrapers (pypi project) to scrape the recipe
# ingredients, instructions and image. Using a prewritten scrape_me function for scraping the websites was easier and 
# had more overall comaptibility then writing the scraper code yourself. It doesnt work on every website, but on many.
# If it is unsuccesfull it flashes an error message and you can try another recipe website.
# Lastly, the third way to add a recipe to a coobook is to create it manually. You can fill a name, the ingredients, instructions, nutritional information and an image to a form. 

# To view all your recipes you can access cookbook.html by the navbar (the navbar hides when scrolling down (JavaScripts)).
# You have an overview of the recipes at the top and when you click on a recipe you get to the recipe card where all the information is displayed. You can also access the original recipe website from cookbook.html or delete a recipe.

# All the data about users, recipes, shopping lists and ingredients (of recipes) are stored in a relational database (recipes_alq.db) and accessed using sql alchemy. The tables are connected using many-to-many relationships to avoid redundancy (f.e. ingredients can belong to multiple recipes and recipes can have multiple different ingredients.)
# For all connections and interactions with the databases I have created seperate files called models.py which contain helper functions being used in auth.py and views.py (main applications for blueprints auth and views).

# Moving on to shoppingList.html, here you can create your own individual shopping list. First you can check any of the recipes of that you want to include the ingredients, then you cann manually remove ingredients that you already have and add ingredients that might be missing (or that you simply want on the shopping list, independet of the recipes).
# You submit and create the shopping list and then JavaScript takes care of gathering the relevant data and send a post
# request to a flask route to store the shopping list in the database.

# Finally you can view all your created shopping lists on savedLists.html. This page is again accessible from the navbar or
# by a button when you create a new shopping lists. The shopping lists are displayed as cards, carrying information like the name, the list items and the date when the list was created.



#### Future improvements and possibilities

# Implementation of an algrotihm that can recommend recipes (and then search for an scrape them) based on ingredients you have at home.

# Visual improvements (Improving CSS files / adding REACT as front end framework)

# Ability to share recipes with a community. Let users interact with each other etc...



#### Further Notes

# Every blueprint has an empty __init__.py application

# Html files are extenstions of layout.html using jinja syntax

# Application is run on a virual enviroment venv

# Helpers.py contains additional helper function like @login_required
