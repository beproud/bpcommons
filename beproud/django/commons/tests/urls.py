#:coding=utf-8:

from django.conf.urls import url, include

from beproud.django.commons.tests.test_views import TestViews

urlpatterns = [
    url(r'', include(TestViews().urls)),
]
