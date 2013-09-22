"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client

client = Client()

class SimpleTest(TestCase):

    def test_home_view(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_article_view(self):
        response = client.get('/1/')
        self.assertEqual(response.status_code, 200)

