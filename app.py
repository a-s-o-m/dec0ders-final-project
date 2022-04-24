from flask_pymongo import PyMongo
from flask import Flask, render_template, request, redirect, url_for
from model import User, get_recipes, get_recipes_test
from sys import stderr


# App variables
app = Flask(__name__)
# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
# Accessed from CONFIG VARS
app.config['MONGO_URI'] = "mongodb+srv://test:test@finalproject.wnetq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app)

user = User('demo@user.com')
recipes = dict()
users = mongo.db.users

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
    global user
    if request.method == 'POST':
        user.add_to_grocery_list(request.form['missing_ing'])
        users.update_one({'email': user.email}, {'$set':{'grocery_list': user.get_grocery_list()}})
    return render_template('grocery-list.html', grocery_list = user.get_grocery_list(), user_email = user.email, email_body = user.get_grocery_list_email_body())

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

@app.route('/email', methods=['POST'])
def email(): 
    # # find user with email
    users = mongo.db.users
    #         #search for username/email in database\
    print(request.form['email'])
    existing_user = users.find_one({'email': request.form['email']})
    global user
    if not existing_user:
        user = User(request.form['email'])
        users.insert_one(user.to_doc())
    # # transform to user object using from_doc method
    else: 
        user = User.from_doc(existing_user)   
    return redirect('/')
    
if __name__=='__main__':
    app.run(debug=True)
