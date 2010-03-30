#:coding=utf-8:
import os

from django.test import TestCase as DjangoTestCase
from django.conf import settings

from django.template.loader import render_to_string

class StringTagsTestCase(DjangoTestCase):

    def setUp(self):
        self.template_dirs = settings.TEMPLATE_DIRS

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.template_dirs
 
    def test_abbrev(self):
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
        output = render_to_string("templatetags_tests/string_tags.html", {"my_data": "1234567890abcdefghi"})
        self.assertEquals(output, "<html><body>1234567...</body></html>\n") 
