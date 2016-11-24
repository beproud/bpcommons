#:coding=utf-8:

from BeautifulSoup import BeautifulSoup

from django.test import TestCase as DjangoTestCase
from django.template.loader import render_to_string

__all__ = (
    'StringTagsTestCase',
    'HtmlTagsTestCase',
    'SwitchTestCase',
)


class StringTagsTestCase(DjangoTestCase):

    def test_abbrev(self):
        output = render_to_string("templatetags_tests/string_tags.html",
                                  {"my_data": "1234567890abcdefghi"})
        self.assertEquals(output, "<html><body>1234567...</body></html>\n")

    def test_abbrev_filter_tag(self):
        output = render_to_string("templatetags_tests/string_tags2.html",
                                  {"my_data": "1234567890abcdefghi"})
        self.assertEquals(output, "<html><body>1234567...</body></html>\n")


class HtmlTagsTestCase(DjangoTestCase):

    def test_to_anchor(self):
        output = render_to_string("templatetags_tests/to_anchor.html", {
            "my_data": u"これはテストデータ。http://www.beproud.jp/これはテストデータ。",
        })

        soup = BeautifulSoup(output)
        anchors = soup.findAll('a')
        self.assertTrue(len(anchors), 1)
        self.assertEquals(anchors[0]['target'], '_blank')
        self.assertEquals(anchors[0]['rel'], 'nofollow')
        self.assertEquals(anchors[0].contents[0], 'http://www.beproud.jp/')

    def test_to_anchortrunc(self):
        output = render_to_string("templatetags_tests/to_anchortrunc.html", {
            "my_data": u"これはテストデータ。http://www.beproud.jp/これはテストデータ。",
        })

        soup = BeautifulSoup(output)
        anchors = soup.findAll('a')
        self.assertTrue(len(anchors), 1)
        self.assertEquals(anchors[0]['target'], '_blank')
        self.assertEquals(anchors[0]['rel'], 'nofollow')
        self.assertEquals(anchors[0].contents[0], 'http://www.b...')


class SwitchTestCase(DjangoTestCase):

    def test_first(self):
        output = render_to_string("templatetags_tests/switch_test.html", {
            'value': 'first',
        })
        self.assertEquals(output, u'<html><body>first value</body></html>\n')

    def test_second(self):
        output = render_to_string("templatetags_tests/switch_test.html", {
            'value': 'second',
        })
        self.assertEquals(output, u'<html><body>second value</body></html>\n')

    def test_default(self):
        output = render_to_string("templatetags_tests/switch_test.html", {
            'value': 'not_exists',
        })
        self.assertEquals(output, u'<html><body>default</body></html>\n')

    def test_missing(self):
        output = render_to_string("templatetags_tests/switch_test.html", {})
        self.assertEquals(output, u'<html><body>default</body></html>\n')