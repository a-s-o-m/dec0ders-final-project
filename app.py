from flask_pymongo import PyMongo
from flask import Flask, render_template, request, redirect, url_for
from model import get_recipes, get_recipes_test

app = Flask(__name__)

# App variables
recipes = dict()


# HOME Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    return render_template('search_page.html')

@app.route('/your-recipes', methods=['GET','POST'])
def user_recipes():
    if request.method == 'POST': # User requests recipes with new ingredients
        global recipes 
        ingredients_input = request.form['ingredients']
        # recipes = get_recipes(ingredients_input)
        recipes = get_recipes_test() # Dummy recipe data for testing purposes

        return render_template('recipes.html', recipes=recipes)
    else:
        return render_template('recipes.html', recipes=recipes)

@app.route('/recipe', methods = ['POST'])
def user_recipe():
    recipe_id = request.form['id']
    recipe = recipes[recipe_id]

    return render_template('recipe.html', recipe=recipe)

@app.route('/email', methods=['GET','POST'])
def email():
    return render_template('email.html')
    
if __name__=='__main__':
    app.run(debug=True)