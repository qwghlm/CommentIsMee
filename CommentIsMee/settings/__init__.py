"""
Settings module. Imports the appropriate level of settings into the app
"""
# Ignore "import all" warnings
#pylint: disable=W0401
import os

ENVIRONMENT = os.getenv("COMMENTISMEE_ENVIRONMENT")

if ENVIRONMENT == "live":
    from .live import *
elif ENVIRONMENT == "staging":
    from .staging import *
else:
    try:
        from .dev import *
    except ImportError:
        pass