# -*- coding: utf-8 -*-
import os

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'beproud.django.commons',
    'testapp',
    'shortcuts_app',
    'models.base',
    'models.fields',
)
MIDDLEWARE = []  # to pass deprecation tcheck
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
ROOT_URLCONF = 'testapp.urls'

TEMPLATES=[{
    'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
}]
SECRET_KEY = '<key>'
USE_TZ = False
