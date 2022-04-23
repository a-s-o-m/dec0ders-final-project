import requests
from collections import defaultdict
class User:
    def __init__(self, email: str):
        '''
        Holds information for the logged in user
        '''
        self.email = email
        self.recipes: Recipe = []
        self.grocery_list: GroceryList = []

    def to_doc(self):
        pass

    @classmethod
    def from_doc(cls, doc):
        pass

class Recipe:
    def __init__(self, id: str, title: str, image: str, total_ingredients: [str], miss_ing: [str], directions: [str], miss_ing_count: str, ing_count: str, servings: str, prep_time: str):
        '''
        Holds the information for the recipes presented to the user
        Arguments:
        id: String containing the recipe id
        title: String containing the title of the recipe
        image: String containing the url for the recipe's image
        total_ingredients: List of Strings containing the total ingredients needed to prepare the recipe
        miss_ing: List of Strings containing the user's necessary missing ingredients
        directions: List of Strings containing the recipe's steps for preparation
        miss_ing_count: String containing the number of missing ingredients
        ing_count: String containing the number of used ingredients
        servings: String containing the number of servings for the current recipe
        prep_time: String containing the number of minutes needed to prepare the recipe
        '''
        parameters = [id, title, image, total_ingredients, miss_ing, directions, miss_ing_count, servings, prep_time]
        
        for parameter in parameters: # Assessing that all parameters are Strings
            if parameter in [total_ingredients, miss_ing, directions]: # Assessing var types for lists parameters
                for val in parameter:
                    if type(val) != str: raise TypeError(f'{val} must be a string.')

            elif type(parameter) != str: raise TypeError(f'{parameter} must be a string.')
        
        self.id = id
        self.title = title
        self.image = image
        self.total_ingredients = total_ingredients
        self.miss_ing = miss_ing
        self.directions = directions
        self.miss_ing_count = miss_ing_count
        self.ing_count = ing_count
        self.servings = servings
        self.prep_time = prep_time


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
    recipe_ing_map = dict() # Mapping recipe title w/user's used and missing ingredients count

    for recipe in recipes_by_ingredient: # Adding ids of found recipes
        recipes_ids.append(str(recipe['id']))
        recipe_ing_map[recipe['title']] = [recipe['missedIngredientCount'],recipe['usedIngredientCount']]

    querystring = {'ids':','.join(recipes_ids),'includeNutrition':'true'} # Query to get recipe information bulk
    recipes_info =  requests.request("GET", recipe_info_url, headers=headers, params=querystring).json() # Recipes w/information

    recipes = {} # To hold Recipe objects used to render the page - key: recipe id. value: Recipe object

    for recipe_info in recipes_info: # Populating Recipe objects
        id = str(recipe_info['id'])
        title = recipe_info['title']
        image = recipe_info['image']
        ingredients = []
        miss_ing = list(set(ingredients) - set(ingredients_input.split(','))) # Recipe ingredients - user ingredients
        directions = []

        if not recipe_info['analyzedInstructions']: continue # Recipe does not contain steps or ingredients
        for step in recipe_info['analyzedInstructions'][0]['steps']: # Populating ingredients and directions lists
            directions.append(step['step']) # Appending directions steps
            for ingredient in step['ingredients']:
                ingredients.append(ingredient['name']) # Appending ingredients

        miss_ing_count = str(recipe_ing_map[recipe_info['title']][0]) # missing ingredients
        ing_count = str(recipe_ing_map[recipe_info['title']][1]) # used ingredients
        servings = str(recipe_info['servings'])
        prep_time = str(recipe_info['readyInMinutes'])

        recipes[id] = Recipe(id, title,image,ingredients,miss_ing,directions,miss_ing_count,ing_count,servings,prep_time) # Appending Recipe object
    
    return recipes

def get_recipes_test():
    '''
    Dummy recipe data for testing purposes
    '''
    return {
        "33":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "13":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "323":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "332":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "333":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "1323":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "3233":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "353":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "373":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400'),
        "3323":Recipe("33","Croque Monsieur","https://spoonacular.com/recipeImages/268203-312x231.jpg",['ham','cheese','bread'],
        ['mayo'],['put cheese on bread','soak sandwich on soap','enjoy'],'1','3','1','400')
    }

class GroceryList:
    def __init__(self):
        '''
        Holds all the missing ingredients that were added to the grocery list for the user
        Arguments:
        groceries_to_get: List of Strings containing the user's necessary missing ingredients
        '''
        self.groceries_dict = defaultdict(int)

    def add_to_grocery_list(self, groceries_to_get: list):
        for grocery in groceries_to_get:
            self.groceries_dict[grocery] += 1
        
    def remove_from_grocery_list(self, groceries_to_remove: list):
        for grocery in groceries_to_remove:
            if self.groceries_dict[grocery] > 1:
                self.groceries_dict[grocery] -= 1
            else: del self.groceries_dict[grocery]

    @classmethod
    def from_doc(cls, doc):
        pass