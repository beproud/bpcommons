import os
import warnings
warnings.filterwarnings("error", module='beproud.django.commons')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from django.apps import apps
apps.populate([
    'testapp',
    'shortcuts_app',
    'beproud.django.commons',
    'models.base',
    'models.fields',
])
