#:coding=utf-8:

from django.test import TestCase as DjangoTestCase
from django.template import Template, Lexer, Parser, get_library, TemplateSyntaxError
from django.template.loader import LoaderOrigin 
from django.template.context import Context

class DataTemplateTagTestCase(DjangoTestCase):


    TEMPLATE_STRING = "<html><body>{% get_my_data 121 as my_data %}{{ my_data }}</body></html>"
    BAD_TEMPLATE_STRING = "<html><body>{% get_my_data 121 my_data %}{{ my_data }}</body></html>"

    def _make_origin(self):
        return LoaderOrigin("Commons Test", lambda x,y: ("<string>", "<string>"), "commons", [])

    def _render_html(self, template_string):
        tag_lib = get_library('commons.tests.test_tags')
        lexer = Lexer(template_string, self._make_origin())
        parser = Parser(lexer.tokenize())
        parser.add_library(tag_lib)
        nodelist = parser.parse()

        return nodelist.render(Context())

    def test_data_template_tag(self):
        self.assertEquals(self._render_html(self.TEMPLATE_STRING), "<html><body>MY DATA</body></html>")
    
    def test_bad_template_tag(self):
        try:
            html = self._render_html(self.BAD_TEMPLATE_STRING)
            self.fail("Expected Fail: %s" % html)
        except TemplateSyntaxError, e:
            pass
