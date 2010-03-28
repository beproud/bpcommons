#:coding=utf-8:
import os

from django.http import HttpRequest
from django.test import TestCase as DjangoTestCase
from django.conf import settings

from commons.views.decorators import * 

@render_to("view_tests/render_to.html")
def myview(request):
    return {"my_value": "MY VALUE"}

class RenderToTestCase(DjangoTestCase):
    def setUp(self):
        self.template_dirs = settings.TEMPLATE_DIRS

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.template_dirs
    
    def test_render_to(self):
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
        resp = myview(HttpRequest())
        self.assertEquals(resp.content, '<html><body>MY VALUE</body></html>\n')

@ajax_request
def my_ajax_view(request):
    return {'my_value': 'MY VALUE'}

class AjaxResponseTestCase(DjangoTestCase):
    def test_ajax_view(self):
        resp = my_ajax_view(HttpRequest())
        self.assertEquals(resp.content, '{"my_value": "MY VALUE"}')
