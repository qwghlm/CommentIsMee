# http://www.crummy.com/software/BeautifulSoup/
# Also needs https://github.com/html5lib
from bs4 import BeautifulSoup

# http://docs.python-requests.org/en/latest/
import requests
from requests.exceptions import RequestException

# https://www.djangoproject.com/
from django.db import models
from django.forms import ModelForm

import json
import re
from pprint import pprint
from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode

class CIFArticle(models.Model):
    """
    Model representing a CIF article
    """
    url = models.URLField(max_length=1024, unique=True)
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

        # Check to see if a Guardian URL
        parsed_url = urlparse(self.url)
        # FIXME be more forgiving!
        if parsed_url.netloc != "www.theguardian.com":
            raise ValueError("Sorry, that does not appear to be a Guardian URL")

        # Use the mobile version if possible - the HTML is better-formed
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

        soup = BeautifulSoup(r.text, "html5lib")
        return soup

    def measure_ego(self):

        # Get an article
        soup = self.download()
        if not soup:
            raise ValueError("Sorry, I could not parse that page properly")

        # Desktop and mobile search for the relevant div
        div = soup.find("div", id="article-body-blocks") or soup.find("div", class_="article-body")
        if not div:
            raise ValueError("Sorry, I could not find relevant HTML in that page")

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
        try:
            data = json.loads(self.scores)
            return data
        except ValueError:
            return {}

    def get_total(self):
        return sum(self.get_word_counts().values())

class CIFArticleForm(ModelForm):
    class Meta:
        model = CIFArticle
        fields = ['url']
