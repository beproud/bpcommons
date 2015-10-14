#:coding=utf-8:

from django import VERSION as DJANGO_VERSION
from django.test import TestCase as DjangoTestCase
from django.template import Template, TemplateSyntaxError
try:
    from django.template import (
        Lexer,
        Parser,
    )
except ImportError:
    from django.template.base import (
        Lexer,
        Parser,
    )

from django.template.loader import LoaderOrigin 
from django.template.context import Context


class BaseTemplateTagTest(object):

    def _make_origin(self):
        return LoaderOrigin("Commons Test", lambda x,y: ("<string>", "<string>"), "commons", [])

    def _render_html(self, template_string, context={}):
        # :(
        if DJANGO_VERSION > (1,7):
            from django.template.base import import_library
            tag_lib = import_library('beproud.django.commons.tests.test_tags')
        elif DJANGO_VERSION > (1,2):
            from django.template import import_library
            tag_lib = import_library('beproud.django.commons.tests.test_tags')
        else:
            from django.template import get_library
            tag_lib = get_library('beproud.django.commons.tests.test_tags')

        lexer = Lexer(template_string, self._make_origin())
        parser = Parser(lexer.tokenize())
        parser.add_library(tag_lib)
        nodelist = parser.parse()

        return nodelist.render(Context(context))

class DataTemplateTagTestCase(BaseTemplateTagTest, DjangoTestCase):

    TEMPLATE_STRING = "<html><body>{% get_my_data 121 as my_data %}{{ my_data }}</body></html>"
    BAD_TEMPLATE_STRING = "<html><body>{% get_my_data 121 my_data %}{{ my_data }}</body></html>"

    def test_data_template_tag(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING), "<html><body>MY DATA</body></html>")
    
    def test_bad_template_tag(self):
        try:
            html = self._render_html(self.BAD_TEMPLATE_STRING)
            self.fail("Expected Fail: %s" % html)
        except TemplateSyntaxError, e:
            pass

class KwargDataTemplateTagTestCase(BaseTemplateTagTest, DjangoTestCase):

    TEMPLATE_STRING1 = "<html><body>{% get_my_kwarg_data 121 as my_data %}{{ my_data }}</body></html>"
    TEMPLATE_STRING2 = "<html><body>{% get_my_kwarg_data 121 status='spam' as my_data %}{{ my_data }}</body></html>"
    TEMPLATE_STRING3 = "<html><body>{% get_my_kwarg_data 121 other='eggs' as my_data %}{{ my_data }}</body></html>"
    TEMPLATE_STRING4 = "<html><body>{% get_my_kwarg_data 121 status='spam' other='eggs' as my_data %}{{ my_data }}</body></html>"
    TEMPLATE_STRING5 = "<html><body>{% get_my_kwarg_data 121 status=spam other=eggs as my_data %}{{ my_data }}</body></html>"

    BAD_TEMPLATE_STRING1 = "<html><body>{% get_my_kwarg_data 121 my_data %}{{ my_data }}</body></html>"
    BAD_TEMPLATE_STRING2 = "<html><body>{% get_my_kwarg_data %}{{ my_data }}</body></html>"
    BAD_TEMPLATE_STRING3 = "<html><body>{% get_my_kwarg_data as my_data %}{{ my_data }}</body></html>"

    BASE_HTML = "<html><body>%s</body></html>"

    def test_kwarg_data_template_tag1(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING1), self.BASE_HTML % "121:None:other")

    def test_kwarg_data_template_tag2(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING2), self.BASE_HTML % "121:spam:other")
    
    def test_kwarg_data_template_tag3(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING3), self.BASE_HTML % "121:None:eggs")

    def test_kwarg_data_template_tag4(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING4), self.BASE_HTML % "121:spam:eggs")

    def test_kwarg_data_template_tag5(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING5, {"spam": "eggs", "eggs": "spam"}), self.BASE_HTML % "121:eggs:spam")

    def test_bad_template_tag1(self):
        try:
            html = self._render_html(self.BAD_TEMPLATE_STRING1)
            self.fail("Expected Fail: %s" % html)
        except TemplateSyntaxError, e:
            pass

    def test_bad_template_tag2(self):
        try:
            html = self._render_html(self.BAD_TEMPLATE_STRING2)
            self.fail("Expected Fail: %s" % html)
        except TemplateSyntaxError, e:
            pass
