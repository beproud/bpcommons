import os
import sys
import unittest
import doctest

def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'commons',
    )
    global_settings.DATABASE_ENGINE = "sqlite3"
    global_settings.DATABASE_NAME = ":memory:"

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    failures = test_runner(['commons'], verbosity=1)
    sys.exit(failures)

if __name__ == '__main__':
    main()
