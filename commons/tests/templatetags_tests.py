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

class HtmlTagsTestCase(DjangoTestCase):

    def setUp(self):
        self.template_dirs = settings.TEMPLATE_DIRS

    def tearDown(self):
        settings.TEMPLATE_DIRS = self.template_dirs
 
    def test_to_anchor(self):
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
        output = render_to_string("templatetags_tests/to_anchor.html", {
            "my_data": u"これはテストデータ。http://www.beproud.jp/これはテストデータ。",
        })
        self.assertEquals(output, u'<html><body>これはテストデータ。<a href="http://www.beproud.jp/" target="_blank" rel="nofollow">http://www.beproud.jp/</a>これはテストデータ。</body></html>\n')

    def test_to_anchortrunc(self):
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
        output = render_to_string("templatetags_tests/to_anchortrunc.html", {
            "my_data": u"これはテストデータ。http://www.beproud.jp/これはテストデータ。",
        })
        self.assertEquals(output, u'<html><body>これはテストデータ。<a href="http://www.beproud.jp/" target="_blank" rel="nofollow">http://www.b...</a>これはテストデータ。</body></html>\n')
