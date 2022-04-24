from flask_pymongo import PyMongo
from flask import Flask, render_template, request, redirect, url_for
from model import User, get_recipes, get_recipes_test

app = Flask(__name__)

# App variables
# find user with email
# transform to user object using from_doc method
user = User('demo@user.com')
recipes = dict()


# HOME Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    return render_template('search_page.html')

@app.route('/grocery-list', methods = ['GET','POST'])
def shopping_list():
    if request.method == 'POST':
        user.add_to_grocery_list(request.form['missing_ing'])
    return render_template('grocery-list.html', grocery_list = user.get_grocery_list())

@app.route('/my-recipes', methods=['GET','POST'])
def user_recipes():
    if request.method == 'POST': # User requests recipes with new ingredients
        global recipes 
        ingredients_input = request.form['ingredients']
        # recipes = get_recipes(ingredients_input)
        recipes = get_recipes_test() # Dummy recipe data for testing purposes

        return render_template('recipes.html', recipes=recipes, new_recipes=True)
    else:
        return render_template('recipes.html', recipes=recipes, new_recipes=False)

@app.route('/recipe', methods = ['POST'])
def user_recipe():
    recipe_id = request.form['id']
    recipe = recipes[recipe_id]

    return render_template('recipe.html', recipe=recipe)

    
if __name__=='__main__':
    app.run(debug=True)
