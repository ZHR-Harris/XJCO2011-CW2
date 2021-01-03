import unittest
from flask import Flask, render_template, request, url_for, redirect, g, flash, jsonify
from app import db
from models import User, Product, Cart_product, Anonymous, Profile, Address, Review
import re
from flask_sqlalchemy import SQLAlchemy



class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # register a new account
        response = self.client.post({{url_for('register')}}, data={
            'email': '111111@qq.com',
            'username': 'hhh',
            'password': '111111',
            'password2': '111111'
        })
        self.assertEqual(response.status_code, 302)

        # login with the new account
        response = self.client.post({{url_for('login')}}, data={
            'email': '111111@qq.com',
            'password': '111111'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search('Shop Now',
                                  response.get_data(as_text=True)))
        self.assertTrue(
            'Email or password is wrong. Please confirm before logging in!' in response.get_data(
                as_text=True))

        # send a confirmation token
        user = User.query.filter_by(email='111111@qq.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token),
                                   follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'You have confirmed your account' in response.get_data(
                as_text=True))

        # log out
        response = self.client.get(url_for('logout'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Registered Customers' in response.get_data(
            as_text=True))

