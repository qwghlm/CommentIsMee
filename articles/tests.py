"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from models import CIFArticle

client = Client()

class SimpleTest(TestCase):

    def test_home_view(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_article_view(self):
        response = client.get('/1/')
        self.assertEqual(response.status_code, 404)

        url = 'http://www.theguardian.com/commentisfree/2013/sep/02/lake-district-wildlife-desert-blame-wordsworth';
        client.post('/', {
        	'url' : url
        	})
        #self.assertEqual(len(CIFArticle.objects.get(url=url)), 1)

        url = 'http://www.theguardian.com/commentisfree/2013/sep/02/lake-district-wildlife-desert-blame-wordsworth?view=mobile';
        client.post('/', {
        	'url' : url
        	})
        #self.assertEqual(len(CIFArticle.objects.get(url=url)), 1)

        # Test form submission when succesful
        response = client.get('/1/')
        self.assertEqual(response.status_code, 200)

        # Test form submission when fails

    def test_article_model(self):

        # Test to make sure non-Guardian URLs do not get stored

        # Test to handle connection errors

        # Test to handle parse errors

        # Test to handle non-article pages

        # Assert scores & word-counts correct

        # Assert correct messages and representations being produced





