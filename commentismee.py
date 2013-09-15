#!/usr/bin/env python

"""
Comment Is Mee
Chris Applegate
(c) 2013
"""

# http://www.crummy.com/software/BeautifulSoup/
# Also needs https://github.com/html5lib
from bs4 import BeautifulSoup

# http://docs.python-requests.org/en/latest/
import requests
from requests.exceptions import RequestException

import re
from pprint import pprint
from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode


class CIFArticle:

    def __init__(self, url):
        self.url = url

    def download(self):
        # Check to see if a Guardian URL
        parsed_url = urlparse(self.url)
        if parsed_url.netloc != "www.theguardian.com":
            print "Error - this is not a Guardian URL, aborting"
            return None

        # Use the mobile version if possible - the HTML is better-formed
        query = dict(parse_qsl(parsed_url.query))
        query["view"] = "mobile"
        url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(query), ""))

        # Fetch the page
        print "Fetching %s..." % url
        try:
            r = requests.get(url)
        except RequestException, e:
            print "Error - could not connect to the URL %s" % url
            return None

        if r.status_code != 200:
            print "Error %s encountered when logging to the URL %s" % (r.status_code, url)
            return None

        return BeautifulSoup(r.text, "html5lib")

    def measure_ego(self):

        # Get an article
        soup = self.download()
        if not soup:
            return {}

        # Desktop and mobile search for the relevant div
        div = soup.find("div", id="article-body-blocks") or soup.find("div", class_="article-body")
        if not div:
            print "Error - could not find relevant HTML in this page"
            return {}

        # Get rid of blockquotes so the count is fair(er)
        for quote in div.find_all("blockquote"):
            quote.decompose()

        # Get author, title and name
        author_tag = soup.find(rel="author")
        author_name = author_tag and author_tag.get_text() or "Unknown Author"

        title_tag = soup.find("title")
        title_text = title_tag and title_tag.get_text().split("|")[0].strip() or "Unknown Title"

        # Cleanup whitespace and convert all to spaces
        text = div.get_text(" ", strip=True) or ""
        text = re.sub("\s+", " ", text)

        # For each keyword, search through and get the score 
        keywords = ("I", "me", "my", "myself", "mine")
        scores = {}
        for keyword in keywords:
            tokens = re.findall(r"\b(%s)\b" % keyword.lower(), text, re.I)
            scores[keyword] = len(tokens)

        meta = {} 
        meta['author'] = author_name
        meta['title'] = title_text
        meta['total'] = sum(scores.values())
        meta['scores'] = scores
        return meta

# Away we go!
article = CIFArticle("http://www.theguardian.com/commentisfree/2013/sep/15/julie-chen-asian-eye-surgery")
print article.measure_ego()
