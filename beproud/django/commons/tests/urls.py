#:coding=utf-8:

from django.conf.urls import url, include

from beproud.django.commons.tests.test_views import TestViews
from beproud.django.commons.tests.test_http import test_json_response

urlpatterns = [
    url(r'', include(TestViews().urls)),
    url(r'json_response', test_json_response),
]
