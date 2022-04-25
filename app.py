from flask_pymongo import PyMongo
from flask import Flask, render_template, request, redirect, url_for
from model import User, get_recipes, get_recipes_test

# App variables
app = Flask(__name__)
# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
# Accessed from CONFIG VARS
app.config['MONGO_URI'] = "mongodb+srv://test:test@finalproject.wnetq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

#Initialize PyMongo
mongo = PyMongo(app)

user = User('')
recipes = dict()

# test

# HOME Route
@app.route('/')
@app.route('/home')
def home():
    global user
    if user.email == '':
        return render_template('home.html', existing_user = None)
    return render_template('home.html', existing_user = user)


'''@app.route('/search')
def search():
    return render_template('search_page.html')
'''
@app.route('/grocery-list', methods = ['GET','POST'])
def shopping_list():
        # # find user with email
    users = mongo.db.users
    global user
    if request.method == 'POST':
        user.add_to_grocery_list(request.form['missing_ing'])
        users.update_one({'email': user.email}, {'$set':{'grocery_list':user.get_grocery_list()}})
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
    #         #search for username/email in database
    existing_user = users.find_one({'email': request.form['email']})
    global user
    if not existing_user:
        user = User(request.form['email'])
        users.insert_one(user.to_doc())
    # # transform to user object using from_doc method
    else: 
        print(existing_user)
        user = User.from_doc(existing_user)  
    return render_template('search_page.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    '''
    if request.method == "POST":
        ingredients = mongo.db.ingredients
        ingredients_input = request.form['ingredients']
        #existing_ingredient = ingredients.find_one({'ingredients':request.form['ingredients']})
        global ingredient   
    if not existing_ingredient:

        #if grocery was valid 
        #if ingredients_input != request.form['ingredients']:
            #add user input to database
            ingredients_input.ingredients(ingredients.to_doc())
            #store user input in session
            ingredient = ingredients.to_document()
            return render_template('recipes.html', ingredients = ingredients)
        return render_template('search_page.html', error='Ingredients can not be found. Please try again.')'''
    return render_template('search_page.html')

    
if __name__=='__main__':
    app.run(debug=True)
