from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class UserAddForm(FlaskForm):
    """Add New User"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class RecipeForm(FlaskForm):
    """Recipe search form"""

    recipe = StringField('Search For...', validators=[DataRequired()])
    diet = SelectField('Choose Diet...', choices=[('none', 'Diet-None'), ('gluten-free', 'Gluten Free'), ('ketogenic', 'Keto'), ('Vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('paleo', 'Paleo'), ('low-fodmap', 'Low FODMAP')])

class CreateCategory(FlaskForm):
    """User can create a recipe category"""

    name = StringField('Category Name', validators=[DataRequired()])
    description = TextAreaField('Description (Opt)')