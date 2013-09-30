#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    DEBUG = (sys.argv[1] == 'runserver')
    if DEBUG:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CommentIsMee.settings_dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CommentIsMee.settings_prod")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
