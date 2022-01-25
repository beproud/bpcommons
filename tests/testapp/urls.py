#:coding=utf-8:

from django.urls import path, include

from .views import TestViews

urlpatterns = [
    path('', include(TestViews().urls)),
]
