import os
from unittest import TestCase

from models import db, User, Recipe, Category

os.environ['DATABASE_URL'] = "postgresql:///recipes_test"

from app import app

db.create_all()


class TestModels(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        db.drop_all()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):

        u = User.signup("testuser", "Password", None)
        db.session.commit()

        user = User.query.filter_by(username = 'testuser').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username,  "testuser")
        self.assertNotEqual(user.password, "Password")
        self.assertTrue(user.password.startswith("$2b$"))

    def test_show_recipe(self):

        response = client.get('/result?recipe=pizza&diet=vegetarian')
        self.assertEqual(response.status_code, 200)
        self.assertIn( recipe_title, response.data) 









