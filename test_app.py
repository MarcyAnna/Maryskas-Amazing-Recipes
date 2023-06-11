import os
from unittest import TestCase

from models import db, User, Recipe, Category

os.environ['DATABASE_URL'] = "postgresql:///recipes_test"

from app import app


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


