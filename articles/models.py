# http://www.crummy.com/software/BeautifulSoup/
# Also needs https://github.com/html5lib
from bs4 import BeautifulSoup

# http://docs.python-requests.org/en/latest/
import requests
from requests.exceptions import RequestException

# https://www.djangoproject.com/
from django.db import models
from django.forms import ModelForm, TextInput
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
        Validate and make sure this is a Guardian URL
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
    url = CIFURLField(max_length=1024, unique=True)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    is_cif = models.BooleanField(default=False)
    scores = models.TextField()
    score = models.FloatField(default=0.0)
    word_count = models.IntegerField(default=0)

    def __repr__(self):
        return "'%s' by %s" % (self.title, self.author)

    def __str__(self):
        return "'%s' by %s" % (self.title, self.author)

    def download(self):
        """
        Download URL of this article and returns a BeautifulSoup object representing it
        """

        # Use the mobile version if possible - the HTML is better-formed
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
            raise ValueError("Sorry, I cannot connect to the URL %s, error %s" % (r.status_code, url))

        # If redirect, save redirected
        self.url = r.url
        soup = BeautifulSoup(r.text, "html5lib")
        return soup

    def measure_ego(self):
        """
        Measure the number of first-person pronouns
        """

        # Get an article
        soup = self.download()
        if not soup:
            raise ValueError("Sorry, I could not parse that page properly")

        # Desktop and mobile search for the relevant div
        div = soup.find("div", id="article-body-blocks") or soup.find("div", class_="article-body")
        if not div:
            raise ValueError("Sorry, I could not find an article in that page")

        # Get rid of blockquotes so the count is fair(er)
        for quote in div.find_all("blockquote"):
            quote.decompose()

        # Get author, title and name
        author_tag = soup.find(rel="author")
        self.author = author_tag and author_tag.get_text() or "Unknown Author"

        title_tag = soup.find("title")
        self.title = title_tag and title_tag.get_text().split("|")[0].strip() or "Unknown Title"

        # Check to see if CIF, either from URL or if the section is labelled as such in the metadata
        section_tag = soup.find("meta", property="article:section")
        section = section_tag and section_tag['content'] or "Unknown Section"
        self.is_cif = self.url.find('commentisfree') > -1 or section.lower() == "comment is free"

        # Cleanup whitespace and convert all to spaces
        text = div.get_text(" ", strip=True) or ""
        text = re.sub("\s+", " ", text)

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

class CIFArticleForm(ModelForm):
    """
    Simplified URL-only form for user to search for
    """
    class Meta:
        model = CIFArticle
        fields = ['url']

