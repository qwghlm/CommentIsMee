from base import *

DEBUG = False # Alternatively, True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # Admins go here
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [
    # Allowed hosts go here
]

SECRET_KEY = '' # Secret key goes here