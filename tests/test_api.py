import unittest
from app import create_app, db
from app.models import User, Role, Post, Comment
import re
from base64 import b64encode
from flask import url_for


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
            'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept':
            'application/json',
            'Content-Type':
            'application/json'
        }

    def test_no_auth(self):
        response = self.client.get(
            '/api/v1/posts/', content_type='application/json')
        self.assertEqual(response.status_code, 401)