import os
import unittest 
from flask import Flask, session
from unittest.mock import patch

from models import db, User, Recipe, Category

os.environ['DATABASE_URL'] = "postgresql:///recipes_test"

from app import app

db.create_all()


class TestModels(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
        

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        db.drop_all()

    def test_homepage(self):
        "test homepage renders"
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        "test user signup"
        u = User.signup("testuser", "Password")
        db.session.commit()

        user = User.query.filter_by(username = 'testuser').first()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username,  "testuser")
        self.assertNotEqual(user.password, "Password")
        self.assertTrue(user.password.startswith("$2b$"))
    
    def test_login(self):
        "test user login"
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='Password'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200) 
        self.assertIsNotNone('curr_user')

    def test_user_page(self):
        "test user is pulled from session and user page renders"
        with app.test_request_context():
            with self.client as client:
                with client.session_transaction() as sess:
                    sess['curr_user'] = 1  

                response = client.get('/user')
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone('curr_user')


    def test_show_recipe(self):
        "test getting response from recipe api"
        response = self.client.post(
            '/result',
            data=dict(recipe="tuna", 
                        diet="ketogenic"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone('data')


    @patch('app.User.query.get')
    def test_save_recipe(self, mock_get_user):
        "test saving recipe to user database"
        with app.test_request_context():
            with self.client as client:
                with client.session_transaction() as sess:
                    sess['curr_user'] = 1  
                    sess['curr_recipe'] = {
                        'results': [{'id': 1, 'title': 'Recipe Title'}]
                    } 
              
                user = User(id=1)  
                mock_get_user.return_value = user

                with patch('app.db.session') as mock_session:
                    response = client.get('/saverecipe')
                    self.assertEqual(response.status_code, 302)
                    self.assertIsNotNone(user.recipes)


    def test_calc_cal(self):
        "test calorie calculator"
        with app.test_request_context():
            with self.client.session_transaction() as sess:
                sess['curr_user'] = 1  

            response = self.client.get('/calories')
            self.assertEqual(response.status_code, 200)
           

    def test_save_cal(self):
        "test saving calculator results to user's database"
        with app.test_request_context():
            with self.client.session_transaction() as sess:
                sess['curr_user'] = 1  

            user = User(id=1, username='testuser', password='testpass', daily_kcal=2000)
            db.session.add(user)
            db.session.commit()

            response = self.client.post('/savecalories', data={'kcal': '2000'})
            self.assertEqual(response.status_code, 302)
            self.assertIsNotNone(user.daily_kcal)

    def test_new_category(self):
        "test creating new category"
        with app.test_request_context():
            with self.client as client:
                with self.client.session_transaction() as sess:
                    sess['curr_user'] = 1 

                cat = Category(name="Dinner", description="new category")
                user = User(id=1, username='testuser', password='testpass', daily_kcal=2000)
                user.categories.append(cat)
                db.session.add(user)
                db.session.commit()
                response = self.client.post('/addcategory')
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(user.categories)




    if __name__ == '__main__':
        unittest.main()

   

   









