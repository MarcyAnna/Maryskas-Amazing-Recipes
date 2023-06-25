import os

from flask import Flask, redirect, render_template, request, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from forms import UserAddForm, LoginForm, CreateCategory, RecipeForm
from models import db, connect_db, User, Recipe, Category

# from secretkey import API_SECRET_KEY

import requests 

API_BASE_URL = "https://api.spoonacular.com/recipes"

# apiKey = API_SECRET_KEY
# for render, API key is in secret storage in app deploy configuration
apiKey = os.environ.get('RECIPE_API_KEY')

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///recipes'))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "1234567890"
# toolbar = DebugToolbarExtension(app)

connect_db(app)
migrate = Migrate(app, db)

# homepage/search routes
@app.route('/')
def homepage():
    """Show Homepage"""

    if 'curr_user' in session:
        user = User.query.get(session['curr_user'])

    else:
        user = None   

    form = RecipeForm() 

    return render_template("homepage.html", user=user, form=form)


@app.route('/result', methods=['GET', 'POST'])
def show_recipe():
    """show recipe search result"""
    print(session)
    if 'curr_user' in session:
        user = User.query.get(session['curr_user'])
    else:
        user = None 
    print(user)
    form = RecipeForm()
    print(form)
    print(apiKey)
    if form.validate_on_submit():
        print("form valid")
        try:
            print("inside try")
            recipe = form.recipe.data
            diet = form.diet.data
            print(recipe, diet)
            res = requests.get(f"{API_BASE_URL}/complexSearch", params={'apiKey': apiKey, 'query': recipe, 'diet': diet, 'instructionsRequired': True, 'number': 1})
            print(res)
            data = res.json()
            session['curr_recipe'] = data

            if data["totalResults"] == 0:
                flash('No recipes found.', 'danger')
                return redirect('/')

            else:
                recipe_title = data["results"][0]["title"]
                recipe_id = data["results"][0]["id"]
                recipe_image = data["results"][0]["image"]
                return render_template('homepage.html', recipe_title = recipe_title, recipe_id = recipe_id, recipe_image = recipe_image, user = user, form=form)
            
        except IntegrityError:
            flash("Please Enter Valid Search", 'danger')
            return redirect('/')



@app.route('/saverecipe')
def save_recipe():
    """Save recipe to user page if user logged in"""

    if 'curr_user' in session:
        user = User.query.get(session['curr_user'])
        data = session['curr_recipe']
        recipe = Recipe(
            recipe_id = data["results"][0]["id"],
            name = data["results"][0]["title"],
            user_id = user.id
        )
        user.recipes.append(recipe)
        db.session.commit()
        session.pop('curr_recipe', None)
        flash('Recipe Saved!', 'success')
        flash('Go to your user page to see details of all your saved recipes')
        return redirect('/')

    else:
        flash('Please Login To Save Recipe!')
        return render_template('homepage.html')

# User routes
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """New User Sign Up"""
    

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/new.html', form=form)
        
        session['curr_user'] = user.id
        return redirect("/")

    else:
        return render_template('users/new.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in to User account"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session['curr_user'] = user.id
            return redirect('/')

        flash("Invalid Username/Password", "danger")
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Log out of user account"""

    if 'curr_user' in session:
        del session['curr_user']

    return redirect('/')

@app.route('/user')
def user_page():
    """Show User saved recipes"""

    user = User.query.get(session['curr_user'])

    return render_template('users/myrecipes.html', user=user)

@app.route('/calories')
def calc_cal():
    """User can factor daily calorie needs"""

    user = User.query.get(session['curr_user'])

    return render_template("caloriecalculator.html", user=user)

@app.route('/savecalories', methods=['GET', 'POST'])
def save_cal():
    """Save calorie to user account"""
  
    user = User.query.get(session['curr_user'])
    cal = request.form["kcal"]
    user.id = user.id
    user.username = user.username
    user.password = user.password
    user.daily_kcal = cal

    if int(cal) > 500 and int(cal) < 5000:
        db.session.commit()
        return redirect('/user')

    else:
        flash('Invalid results for calorie count. Please check your entries and reenter correct information', 'danger')
        return render_template("caloriecalculator.html", user=user)


# recipe/category routes
@app.route('/addcategory', methods=['GET', 'POST'])
def new_category():
    """User add new category to account"""

    form = CreateCategory()
    user = User.query.get(session['curr_user'])

    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            )
        user.categories.append(category)
        db.session.commit()
        return redirect('/user')

    return render_template('category.html', form=form, user=user)

@app.route('/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """User delete category"""

    cat = Category.query.get(category_id)
    db.session.delete(cat)
    db.session.commit()

    return redirect("/user")

@app.route('/<int:category_id>/addrecipe', methods=['GET', 'POST'])
def add_recipe_to_cat(category_id):
    """add recipe to a category"""

    user = User.query.get(session['curr_user'])
    cat = Category.query.get(category_id)
    recipeId = request.args.get('recipe_cat')
    recipe = Recipe.query.get(recipeId)
    recipe.id = recipe.id
    recipe.recipe_id = recipe.recipe_id
    recipe.name = recipe.name
    recipe.user_id = recipe.user_id
    recipe.category_id = category_id
    db.session.add(recipe)
    db.session.commit()

    return redirect('/user')


@app.route('/<int:recipe_id>')
def view_recipe(recipe_id):
    """View Recipe details"""

    user = User.query.get(session['curr_user'])
    recipe_id = recipe_id
    res = requests.get(f"{API_BASE_URL}/{recipe_id}/information", params={"apiKey": apiKey, "includeNutrition": True})
    data = res.json()
    ingredients = parse_ingredients(data)
    recipe_title = data["title"]
    cal = data["nutrition"]["nutrients"][0]["amount"]
    sourceUrl = data["sourceUrl"]
    sourceUrlSplit = sourceUrl[7:]
    sourceName = data["sourceName"]

    return render_template("recipe.html", recipe_title=recipe_title, cal=cal, ingredients=ingredients, sourceUrl=sourceUrl, sourceUrlSplit=sourceUrlSplit, sourceName=sourceName, user=user, recipe_id=recipe_id)


#stand-alone functions
def parse_ingredients(data):
    """Parse ingredients by name"""
    listIngredients = []
    for x in range( len(data["extendedIngredients"])):
        original = data["extendedIngredients"][x]["original"]
        listIngredients.append(original)

    return(listIngredients)



