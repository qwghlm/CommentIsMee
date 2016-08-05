from django.db import models
from urlparse import urlparse, urlunparse

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