#:coding=utf-8:

from django.conf.urls import re_path, include

from .views import TestViews

urlpatterns = [
    re_path(r'', include(TestViews().urls)),
]
