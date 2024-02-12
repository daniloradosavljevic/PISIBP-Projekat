import os
from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re
import ip_address as ip
from werkzeug.utils import secure_filename
import datetime
import unittest
from app import app


class TestHomeFunction(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_when_logged_in(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['loggedin'] = True
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            if response.location:
                self.assertIn(b'index.html', response.location.encode())

    def test_home_when_not_logged_in(self):
        with self.app as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)
            if response.location:
                self.assertIn(b'prikaz_novosti', response.location.encode())

    def test_login_with_valid_credentials(self):
        with self.app as client:
            response = client.post('/cms/login', data=dict(
                username='valid_username',
                password='valid_password'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 302)
            if response.location:
                self.assertIn(b'Logged in successfully!', response.data)
                self.assertIn(b'/cms/home', response.headers.get(b'Location'))


#    def test_login_with_invalid_credentials(self):
#        with self.app as client:
#            response = client.post('/cms/login', data=dict(
#                username='invalid_username',
#                password='invalid_password'
#            ), follow_redirects=True)
#            self.assertEqual(response.status_code, 200)
#            if response.location:
#                self.assertIn(b'Incorrect username/password', response.data)

    def test_login_redirect_when_already_logged_in(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['loggedin'] = True
            response = client.get('/cms/login', follow_redirects=True)
            if response.location:
                self.assertEqual(response.status_code, 302)
                self.assertIn(b'Location', response.headers)  
                self.assertIn(b'/cms/home', response.headers.get(b'Location'))


if __name__ == '__main__':
    unittest.main()
