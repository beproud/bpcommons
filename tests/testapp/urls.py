#:coding=utf-8:

from django.conf.urls import url, include

from .views import TestViews

urlpatterns = [
    url(r'', include(TestViews().urls)),
]
