from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    daily_kcal = db.Column(
        db.Integer
    )

    recipes = db.relationship('Recipe')

    categories = db.relationship('Category')

    @classmethod
    def signup(cls, username, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Recipe(db.Model):
    """Recipe Model for adding a recipe to user's account"""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    recipe_id = db.Column(
        db.Integer,
        nullable=False
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        nullable=False,
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', ondelete="cascade")
    )

    # rating_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('ratings.id')
    # )

    users = db.relationship('User', foreign_keys=[user_id])

    categories = db.relationship('Category', foreign_keys=[category_id])

    # ratings = db.relationship('Rating', foreign_keys=[rating_id])

class Category(db.Model):
    """Category Model for user to create a specific category to save recipes under"""

    __tablename__ = 'categories'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = db.Column(
        db.String(20),
        nullable=False,
    )

    description = db.Column(
        db.Text,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    users = db.relationship('User', foreign_keys=[user_id])


# class Rating(db.Model):
#     """Rating Model for user to give feedback on a recipe"""

#     __tablename__ = 'ratings'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True,
#     )

#     rating_stars = db.Column(
#         db.Integer,
#         nullable=False
#     )

#     comment = db.Column(
#         db.Text
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id'),
#         nullable=False
#     )

#     recipe_id = db.Column(
#         db.Integer,
#         db.ForeignKey('recipes.id'),
#         nullable=False
#     ) 

#     users = db.relationship('User', foreign_keys=[user_id])

#     recipes = db.relationship('Recipe', foreign_keys=[recipe_id])

# class Category_Recipes(db.Model):
#     """Joins the recipes with the category they fall under"""

#     __tablename__ = 'category_recipe'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True,
#     )

#     category_id = db.Column(
#         db.Integer,
#         db.ForeignKey('categories.id'),
#         nullable=False
#     )

#     recipe_id = db.Column(
#         db.Integer,
#         db.ForeignKey('recipes.id'),
#         nullable=False
#     )

#     recipes = db.relationship('Recipe')

#     categories = db.relationship('Category')

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
















    