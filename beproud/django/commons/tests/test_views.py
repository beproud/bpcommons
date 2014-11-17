#:coding=utf-8:

import os

from django.conf.urls import url, patterns
from django.http import HttpRequest, HttpResponse
from django.test import TestCase as DjangoTestCase
from django.conf import settings

from beproud.django.commons.views.decorators import render_to, ajax_request
from beproud.django.commons.http import JSONResponse
from beproud.django.commons.views import Views


class TestViews(Views):
    def test(self, request):
        return HttpResponse("OK")

    def get_urls(self):
        urls = super(TestViews, self).get_urls()
        my_urls = patterns(
            '',
            url(
                r'^test$',
                self.test,
                name='testview_test',
            ),
        )
        return my_urls + urls


class ClassesTestCase(DjangoTestCase):
    def test_simple(self):
        response = self.client.get("/test")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "OK")


@render_to("view_tests/render_to.html")
def myview(request):
    return {"my_value": "MY VALUE"}


@render_to("view_tests/render_to.html")
def myview2(request):
    return HttpResponse("Error!")


class RenderToTestCase(DjangoTestCase):
    def setUp(self):
        self.template_dirs = settings.TEMPLATE_DIRS

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.template_dirs

    def test_render_to(self):
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
        resp = myview(HttpRequest())
        self.assertEquals(resp.content, '<html><body>MY VALUE</body></html>\n')

    def test_render_to_httpresponse(self):
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
        resp = myview2(HttpRequest())
        self.assertEquals(resp.content, 'Error!')


@ajax_request
def my_ajax_view(request):
    return {'my_value': 'MY VALUE'}


@ajax_request
def my_ajax_view2(request):
    return HttpResponse("Error!")


class AjaxResponseTestCase(DjangoTestCase):
    def test_ajax_view(self):
        resp = my_ajax_view(HttpRequest())
        self.assertEquals(resp["content-type"], 'application/json')
        self.assertEquals(resp.content, '{"my_value": "MY VALUE"}')

    def test_ajax_view_httpresponse(self):
        resp = my_ajax_view2(HttpRequest())
        self.assertEquals(resp["content-type"], 'text/html; charset=utf-8')
        self.assertEquals(resp.content, 'Error!')


def my_json_view(request):
    return JSONResponse({"msg": "テスト"}, status=400)


class JSONResponseTestCase(DjangoTestCase):
    def test_json_view(self):
        resp = my_json_view(HttpRequest())
        self.assertEquals(resp["content-type"], 'application/json')
        self.assertEquals(resp.content, r'{"msg": "\u30c6\u30b9\u30c8"}')
        self.assertEquals(resp.status_code, 400)
