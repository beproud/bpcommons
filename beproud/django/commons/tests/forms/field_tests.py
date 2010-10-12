#:coding=utf-8:

from django.test import TestCase as DjangoTestCase

from django.forms import Form

from beproud.django.commons.forms import *
from beproud.django.commons.forms.widgets import *

class EmailTestForm(Form):
    email = EmailField(label="email")

class EmailFieldTest(DjangoTestCase):

    def test_basic_email(self):
        form = EmailTestForm({"email": "spam@eggs.com"})
        self.assertTrue(form.is_valid())

    def test_keitai_email(self):
        form = EmailTestForm({"email": "-spam..eggs-@softbank.ne.jp"})
        self.assertTrue(form.is_valid())

        form = EmailTestForm({"email": ".*&$.-spam..!!eggs!!-.*.@ezweb.ne.jp"})
        self.assertTrue(form.is_valid())

    def test_plus_email(self):
        form = EmailTestForm({"email": "spam+extra@eggs.com"})
        self.assertTrue(form.is_valid())

class JSONTestForm(Form):
    json = JSONField(label="json")

class JSONFormFieldTest(DjangoTestCase):

    def test_json(self):
        form = JSONTestForm({"json": '{"spam": "eggs"}'})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["json"], {"spam": "eggs"})

    def test_bad_json(self):
        form = JSONTestForm({"json": '{"spam": "eggs"'})
        self.assertFalse(form.is_valid())

class JSONWidgetTest(DjangoTestCase):
    def test_jsonwidget(self):
        form = JSONTestForm({"json": '{"spam": "eggs"}'})
        self.assertEquals(str(form), '<tr><th><label for="id_json">json:</label></th><td><textarea id="id_json" rows="10" cols="40" name="json">{&quot;spam&quot;: &quot;eggs&quot;}</textarea></td></tr>')

    def test_render(self):
        widget = JSONWidget()
        self.assertEquals(
            widget.render("json", {"spam": "eggs"}),
            '<textarea rows="10" cols="40" name="json">{\n  &quot;spam&quot;: &quot;eggs&quot;\n}</textarea>');

