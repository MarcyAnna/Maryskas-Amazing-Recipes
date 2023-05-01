from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length

class UserAddForm(FlaskForm):
    """Add New User"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class CreateCategory(FlaskForm):
    """User can create a recipe category"""

    name = StringField('Category Name', validators=[DataRequired()])
    description = TextAreaField('Description (Opt)')