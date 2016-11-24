#:coding=utf-8:

from django.http import HttpRequest
from django.test import TestCase as DjangoTestCase


class ClassesTestCase(DjangoTestCase):
    def test_simple(self):
        response = self.client.get("/test")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, "OK")


class RenderToTestCase(DjangoTestCase):

    def test_render_to(self):
        from testapp.views import myview
        resp = myview(HttpRequest())
        self.assertEquals(resp.content, '<html><body>MY VALUE</body></html>\n')

    def test_render_to_httpresponse(self):
        from testapp.views import myview2
        resp = myview2(HttpRequest())
        self.assertEquals(resp.content, 'Error!')


class AjaxResponseTestCase(DjangoTestCase):

    def test_ajax_view(self):
        from testapp.views import my_ajax_view
        resp = my_ajax_view(HttpRequest())
        self.assertEquals(resp["content-type"], 'application/json')
        self.assertEquals(resp.content, '{"my_value": "MY VALUE"}')

    def test_ajax_view_httpresponse(self):
        from testapp.views import my_ajax_view2
        resp = my_ajax_view2(HttpRequest())
        self.assertEquals(resp["content-type"], 'text/html; charset=utf-8')
        self.assertEquals(resp.content, 'Error!')
