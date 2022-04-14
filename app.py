from flask import Flask, render_template,request,url_for
import requests

app = Flask(__name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': "7557410a9bmsh5338d5c3d59ebdbp1c1418jsn9d0fd7a3e354",
  }

random_joke = "food/jokes/random"
find = "recipes/findByIngredients"
randomFind = "recipes/random"

@app.route('/')
def index():
    return render_template('search_page.html')

@app.route('/recipes')
def get_recipes():
    if (str(request.args['ingridients']).strip() != ""):
      # If there is a list of ingridients -> list
      querystring = {"number":"5","ranking":"1","ignorePantry":"false","ingredients":request.args['ingridients']}
      response = requests.request("GET", url + find, headers=headers, params=querystring).json()
      return render_template('recipes.html', recipes=response)
    else:
      # Random recipes
      querystring = {"number":"5"}
      response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
      print(response)
      return render_template('recipes.html', recipes=response['recipes'])

if __name__=='__main__':
    app.run(debug=True)