#:coding=utf-8:
from django.conf.urls.defaults import *
from django.conf import settings

from beproud.django.commons.tests.views_tests import TestViews

urlpatterns = patterns('',
    (r'', include(TestViews().urls)),
    (r'json_response', 'beproud.django.commons.tests.http.test_json_response'),
)
