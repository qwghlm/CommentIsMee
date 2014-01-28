from settings import *

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

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''