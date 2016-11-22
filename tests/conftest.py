import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from django.apps import apps
apps.populate([
    'testapp',
    'shortcuts_app',
    'beproud.django.commons',
    'models.base',
    'models.fields',
])
