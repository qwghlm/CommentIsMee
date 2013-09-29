# http://www.crummy.com/software/BeautifulSoup/
# Also needs https://github.com/html5lib
from bs4 import BeautifulSoup

# http://docs.python-requests.org/en/latest/
import requests
from requests.exceptions import RequestException

# https://www.djangoproject.com/
from django.db import models
from django.forms import ModelForm, TextInput, URLField
from django.core.exceptions import ValidationError

import json
import re
from pprint import pprint
from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode


class CIFURLField(models.URLField):

    def to_python(self, value):
        """
        Get rid of query and anchor when saving URL canonically
        """
        parsed_url = urlparse(value)
        url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", ""))
        return url

    def validate(self, value, form):
        """
        Validate and make sure this is a valid URL
        """
        super(CIFURLField, self).validate(value, form)
        parsed_url = urlparse(value)

        valid_domains = ("theguardian.com", "guardian.co.uk", "gu.com")
        for domain in valid_domains:
            if parsed_url.netloc.find(domain) > -1:
                return

        raise ValidationError(
            "Sorry, %s does not appear to be a Guardian URL" % value,
            code="invalid")

class CIFArticle(models.Model):
    """
    Model representing a CIF article
    """
    url = CIFURLField(max_length=1024)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    is_cif = models.BooleanField(default=False)
    scores = models.TextField()
    score = models.FloatField(default=0.0)
    word_count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'"%s" by %s' % (self.title, self.author)

    def __repr__(self):
        return self.__unicode__().encode('utf8')

    def __str__(self):
        return self.__repr__()

    def download_page(self):
        """
        Download URL of this article and returns the HTML of that page as a string
        """

        # Use the mobile version - the HTML is better-formed
        parsed_url = urlparse(self.url)
        query = dict(parse_qsl(parsed_url.query))
        query["view"] = "mobile"
        url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(query), ""))

        # Fetch the page
        try:
            r = requests.get(url)
        except RequestException, e:
            raise ValueError("Sorry, I cannot connect to the URL %s" % url)

        if r.status_code != 200:
            raise ValueError("Sorry, I cannot connect to the URL %s, error %s" % (url, r.status_code))

        # If redirect, save redirected
        self.url = r.url
        return r.text

    def extract_article(self):
        """
        Extracts article out of a downloaded URL as text
        """
        # Get an article
        html = self.download_page()
        soup = BeautifulSoup(html, "html5lib")
        if not soup:
            raise ValueError("Sorry, I could not parse that page properly")

        # Get author, title and name
        author_tag = soup.find(rel="author")
        self.author = author_tag and author_tag.get_text() or "Unknown Author"

        title_tag = soup.find("title")
        self.title = title_tag and title_tag.get_text().split("|")[0].strip() or "Unknown Title"

        # Check to see if CIF, either from URL or if the section is labelled as such in the metadata
        section_tag = soup.find("meta", property="article:section")
        section = section_tag and section_tag['content'] or "Unknown Section"
        self.is_cif = self.url.find('commentisfree') > -1 or section.lower() == "comment is free"

        # Desktop and mobile search for the relevant div
        div = soup.find("div", id="article-body-blocks") or soup.find("div", class_="article-body")
        if not div:
            raise ValueError("Sorry, I could not find an article in that page")

        # Get rid of blockquotes so the count is fair(er)
        for quote in div.find_all("blockquote"):
            quote.decompose()

        # Cleanup whitespace, convert all to spaces and then return
        text = div.get_text(" ", strip=True) or ""
        text = re.sub("\s+", " ", text)
        return text

    def measure_ego(self):
        """
        Measure the number of first-person pronouns
        """
        text = self.extract_article()

        # For each keyword, search through and get the score 
        keywords = ("I", "me", "my", "myself", "mine")
        scores = {}
        for keyword in keywords:
            tokens = re.findall(r"\b(%s)\b" % keyword.lower(), text, re.I)
            scores[keyword] = len(tokens)

        self.word_count = len(text.split(' '))
        self.scores = json.dumps(scores)
        self.score = round(1000 * float(self.get_total())/float(self.word_count), 2)

    def get_word_counts(self):
        """
        Get word counts as JSON, with fallback for legacy versions
        """
        try:
            data = json.loads(self.scores)
            return data
        except ValueError:
            return {}

    def get_total(self):
        """
        Get total number of words from our word count breakdown
        """
        return sum(self.get_word_counts().values())

    def get_message(self):
        """
        Return a sarcastic message depending on the quality of the article
        """
        messages = {
            0 : "Not a single word! How very worldly and refined.",
            5 : "The odd self-mention in there, but we can let it pass.",
            10 : "Not great, but at least you'll get a word in edgeways sometimes.",
            20 : "Might have a bit of trouble getting their head through the door from time to time.",
            40 : "Someone's 'I' key on their keyboard is going to need replacing very soon.",
            60 : "That article is going to get very boring very quickly. Unless you wrote it.",
            100 : "I bet the person who wrote this has a picture of themselves on their desk.",
            1000 : "More than a tenth of the words! The world must literally revolve around this person.",
        }
        message_key = min([key for key in messages.keys() if self.score <= key])
        return messages[message_key]

    def severity(self):
        """

        """
        messages = {
            0 : "none",
            10 : "low",
            20 : "medium",
            40 : "high",
            80 : "maximum",
        }
        message_key = min([key for key in messages.keys() if self.score <= key])
        return messages[message_key]

class CIFArticleForm(ModelForm):
    """
    Simplified URL-only form for user to search for
    """
    attrs = {
        'class' : 'span7',
        'placeholder' : 'Type or paste a CIF link here'
    }
    url = URLField(widget=TextInput(attrs=attrs))
    class Meta:
        model = CIFArticle
        fields = ['url']

