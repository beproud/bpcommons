#:coding=utf-8:

from django.http import HttpRequest
from django.test import TestCase as DjangoTestCase


class ClassesTestCase(DjangoTestCase):
    def test_simple(self):
        response = self.client.get("/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")


class RenderToTestCase(DjangoTestCase):

    def test_render_to(self):
        from testapp.views import myview
        resp = myview(HttpRequest())
        self.assertEqual(resp.content, b'<html><body>MY VALUE</body></html>\n')

    def test_render_to_httpresponse(self):
        from testapp.views import myview2
        resp = myview2(HttpRequest())
        self.assertEqual(resp.content, b'Error!')


class AjaxResponseTestCase(DjangoTestCase):

    def test_ajax_view(self):
        from testapp.views import my_ajax_view
        resp = my_ajax_view(HttpRequest())
        self.assertEqual(resp["content-type"], 'application/json')
        self.assertEqual(resp.content, b'{"my_value": "MY VALUE"}')

    def test_ajax_view_httpresponse(self):
        from testapp.views import my_ajax_view2
        resp = my_ajax_view2(HttpRequest())
        self.assertEqual(resp["content-type"], 'text/html; charset=utf-8')
        self.assertEqual(resp.content, b'Error!')
