
import requests
from collections import defaultdict
from sys import stderr

class User:
    def __init__(self, email: str):
        '''
        Holds information for the logged in user
        '''
        self.email = email
        self.recipes: Recipe = []
        self.grocery_list = defaultdict(int)


    def add_to_grocery_list(self, groceries_to_get):
        for grocery in groceries_to_get.split(','):
            self.grocery_list[grocery] += 1

    #invoked if recipe is removed or marked as done  
    def remove_from_grocery_list(self, groceries_to_remove: list):
        for grocery in groceries_to_remove:
            if self.grocery_list[grocery] > 1:
                self.grocery_list[grocery] -= 1
            else: del self.grocery_list[grocery]
        # update grocery list in mongodb

    def get_grocery_list(self):
        return self.grocery_list

    def get_grocery_list_email_body(self):
        body = ''
        for grocery, quantity in self.grocery_list.items():
            body += f"{grocery} (x{quantity}) %0D%0A"
        return body

    def to_doc(self):
        return {
            'email': self.email,
            'recipes': self.recipes,
            'grocery_list': self.grocery_list
        }

    @classmethod
    def from_doc(cls, doc): 
        cls.email = doc['email']
        cls.recipes = doc['recipes']
        cls.grocery_list = doc['grocery_list']       

class Recipe:
    def __init__(self, id, title, image, total_ingredients, missing_ing, directions, missing_ing_count, ing_count, servings, prep_time, likes):
        '''
        Holds the information for the recipes presented to the user
        Arguments:
        id: String containing the recipe id
        title: String containing the title of the recipe
        image: String containing the url for the recipe's image
        total_ingredients: List of Strings containing the total ingredients needed to prepare the recipe
        missing_ing: List of Strings containing the user's missing ingredients
        directions: List of Strings containing the recipe's steps for preparation
        missing_ing_count: String containing the number of missing ingredients
        ing_count: String containing the number of used ingredients
        servings: String containing the number of servings for the current recipe
        prep_time: String containing the number of minutes needed to prepare the recipe
        likes: String containing the number of recipe likes
        '''
        parameters = [id, title, image, total_ingredients, missing_ing, directions, missing_ing_count, servings, prep_time, likes]
        
        for parameter in parameters: # Assessing that all parameters are Strings
            if parameter in [total_ingredients, missing_ing, directions]: # Assessing var types for lists parameters
                for val in parameter:
                    if type(val) != str: raise TypeError(f'{val} must be a string.')

            elif type(parameter) != str: raise TypeError(f'{parameter} must be a string.')
        
        self.id = id
        self.title = title
        self.image = image
        self.total_ingredients = total_ingredients
        self.missing_ing = missing_ing
        self.directions = directions
        self.missing_ing_count = missing_ing_count
        self.ing_count = ing_count
        self.servings = servings
        self.prep_time = prep_time
        self.likes = likes


headers = { # Spoonacular API host url and key
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': "7557410a9bmsh5338d5c3d59ebdbp1c1418jsn9d0fd7a3e354",
  }
# Spoonacular endpoints urls
find_by_ingredients_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
recipe_info_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/informationBulk"

def get_recipes(ingredients_input: str):
    '''
    Takes the ingredients given by the user and
    returns a list of Recipe objects found by the Spoonacular API
    Arguments:
    ingredients: String containing the ingredients given by the user
    '''
    ingredients_input = ingredients_input.replace(' ', '') # Removing whitespace from ingredients input
    querystring = {"number":"7","ranking":"2","ignorePantry":"false","ingredients":ingredients_input} # Query to get recipes by ingredients
    recipes_by_ingredient = requests.request("GET", find_by_ingredients_url, headers=headers, params=querystring).json() # Recipes found

    recipes_ids = [] # To hold recipes id for another query in order to get recipes' complete information bulk 
    recipe_like_map = dict() # Mapping recipe id to recipe num of likes

    for recipe in recipes_by_ingredient: # Adding ids of found recipes
        recipes_ids.append(str(recipe['id']))
        recipe_like_map[str(recipe['id'])] = recipe['likes']

    querystring = {'ids':','.join(recipes_ids),'includeNutrition':'true'} # Query to get recipe information bulk
    recipes_info =  requests.request("GET", recipe_info_url, headers=headers, params=querystring).json() # Recipes w/information

    recipes = {} # To hold Recipe objects used to render the page - key: recipe id. value: Recipe object

    for recipe_info in recipes_info: # Populating Recipe objects
        user_ingredients = ingredients_input.split(',')
        id = str(recipe_info['id'])
        title = recipe_info['title']
        image = recipe_info['image']
        ing_count = str(len(user_ingredients)) # num of user ingredients
        ingredients = []
        
        directions = []

        if not recipe_info['analyzedInstructions']: continue # Recipe does not contain steps or ingredients
        for step in recipe_info['analyzedInstructions'][0]['steps']: # Populating ingredients and directions lists
            directions.append(step['step']) # Appending directions steps
            for ingredient in step['ingredients']:
                ingredients.append(ingredient['name']) # Appending ingredients
                
        missing_ing = list(set(ingredients) - set(user_ingredients)) # Recipe ingredients - user ingredients
        missing_ing_count = str(len(missing_ing)) # missing ingredients
        
        servings = str(recipe_info['servings'])
        prep_time = str(recipe_info['readyInMinutes'])
        likes = str(recipe_like_map[id])

        recipes[id] = Recipe(id,title,image,user_ingredients,missing_ing,directions,missing_ing_count,ing_count,servings,prep_time,likes) # Appending Recipe object
    
    return recipes

def get_recipes_test():
    '''
    Dummy recipe data for testing purposes
    '''
    return {
        "1":Recipe("1","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['salt & pepper','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "2":Recipe("2","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','mayonesse'],
        [],['put cheese on bread','soak sandwich on soap','enjoy'],'0','3','1','35','10'),
        "3":Recipe("3","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo', 'honey mustard', 'mayo', 'mayo' ],['put cheese on bread put cheese on bread put cheese on bread put cheese on bread put cheese on bread put cheese on bread put cheese on breadput cheese on bread put cheese on bread put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "4":Recipe("4","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham & cheese','milk','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "5":Recipe("5","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "6":Recipe("6","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "7":Recipe("7","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "8":Recipe("8","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "9":Recipe("9","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10'),
        "10":Recipe("10","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400','10')
    }