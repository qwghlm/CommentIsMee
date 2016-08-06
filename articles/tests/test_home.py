from django.test import TestCase, Client

class HomeTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

        # Test for existence of form
        # Test for existence of articles already in the database

    def test_missing_page(self):
        # Check an individual URL
        # Test for existence of page & 200 code
        pass

    def test_missing_page(self):
        response = self.client.get('/1/')
        self.assertEqual(404, response.status_code)

    def test_post(self):
        # Post a URL to the site
        # Test that it gets added to the database and values match
        # Test that the URL is suitable trimmed
        # Test we get redirect to its page
        pass

    def test_invalid_post(self):
        # Make a bad request to the site
        # Test that no change to the database
        # Test for URL error on form
        pass

    def test_invalid_url(self):
        # Make a valid request but not a Guardian page
        # Test that no change to the database
        # Test for URL error on form
        pass

    def test_invalid_url(self):
        # Make a valid request but not valid HTML page
        # Test that no change to the database
        # Test for URL error on form
        pass


# TODO Test for word count of various texts
