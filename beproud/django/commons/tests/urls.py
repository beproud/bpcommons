#:coding=utf-8:

from django.conf.urls import patterns, include

from beproud.django.commons.tests.test_views import TestViews

urlpatterns = patterns(
    '',
    (r'', include(TestViews().urls)),
    (r'json_response', 'beproud.django.commons.tests.test_http.test_json_response'),
)
