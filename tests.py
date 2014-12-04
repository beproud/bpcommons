#:coding-utf-8:

import os
import sys
import django


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.SECRET_KEY = 'snakeoil'

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'beproud.django.commons.tests.test_shortcuts.shortcuts_app',
        'beproud.django.commons.tests.models.base',
        'beproud.django.commons.tests.models.fields',
        'beproud.django.commons',
    )

    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

    # For MySQL
    # NOTE: Django < 1.7 の場合は bpcommons データベースは存在しないとダメ
    #global_settings.DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.mysql',
    #        'NAME': 'bpcommons',
    #        'USER': '<user>',
    #        'PASSWORD': '<password>',
    #        'HOST': '<host>,
    #        #'PORT': '',
    #    }
    #}

    global_settings.ROOT_URLCONF = 'beproud.django.commons.tests.urls'

    if django.VERSION > (1, 7):
        django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 6):
        # See: https://docs.djangoproject.com/en/1.6/topics/testing/overview/#running-tests
        tests = ['beproud.django.commons']
    else:
        tests = ['commons']

    test_runner = test_runner(interactive=False)
    failures = test_runner.run_tests(tests)

    sys.exit(failures)

if __name__ == '__main__':
    main()
