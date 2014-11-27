#:coding=utf-8:

from django.test import TestCase as DjangoTestCase

from django.forms import Form

from beproud.django.commons.forms import EmailField, JSONField
from beproud.django.commons.forms.widgets import JSONWidget

__all__ = (
    'EmailFieldTest',
    'JSONFormFieldTest',
    'JSONWidgetTest',
)


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

    def test_multi_email(self):
        form = EmailTestForm({"email": "aaa spam+extra@eggs.com email@email.com"})
        self.assertFalse(form.is_valid())


class JSONFormFieldTest(DjangoTestCase):

    def test_json(self):
        class JSONTestForm(Form):
            json = JSONField(label="json")

        form = JSONTestForm({"json": '{"spam": "eggs"}'})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["json"], {"spam": "eggs"})

    def test_json_fail(self):
        class JSONTestForm(Form):
            json = JSONField(label="json")

        form = JSONTestForm({"json": '{"spam": "eggs"'})
        self.assertFalse(form.is_valid())

    def test_to_python(self):
        class JSONTestForm(Form):
            json = JSONField(label="json")

        form = JSONTestForm({"json": {"spam": "eggs"}})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["json"], {"spam": "eggs"})

    def test_to_python_with_max_length(self):
        class JSONTestForm(Form):
            json = JSONField(label="json", max_length=100)

        form = JSONTestForm({"json": {"spam": "eggs"}})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["json"], {"spam": "eggs"})

    def test_to_python_with_max_length_fail(self):
        class JSONTestForm(Form):
            json = JSONField(label="json", max_length=5)

        form = JSONTestForm({"json": {"spam": "eggs"}})
        self.assertFalse(form.is_valid())

    def test_to_python_empty_values_required(self):
        class JSONTestForm(Form):
            json = JSONField(label="json", required=True)

        form = JSONTestForm({'json': '{}'})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["json"], {})

        form = JSONTestForm({'json': {}})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["json"], {})

        form = JSONTestForm({'json': ''})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors.get('json'), form.fields['json'].error_messages['required'])

    def test_to_python_not_required(self):
        class JSONTestForm(Form):
            json = JSONField(label="json", required=False)

        form = JSONTestForm({'json': ''})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['json'] is None)


class JSONWidgetTest(DjangoTestCase):
    def test_jsonwidget(self):
        class JSONTestForm(Form):
            json = JSONField(label="json")

        form = JSONTestForm({"json": '{"spam": "eggs"}'})
        rendered_form = str(form)
        self.assertTrue("<tr" in rendered_form)
        self.assertTrue("</tr>" in rendered_form)
        self.assertTrue("<th" in rendered_form)
        self.assertTrue("</th>" in rendered_form)
        self.assertTrue("<textarea" in rendered_form)
        self.assertTrue('name="json"' in rendered_form)
        self.assertTrue('id="id_json"' in rendered_form)
        self.assertTrue("{&quot;spam&quot;: &quot;eggs&quot;}" in rendered_form)

    def test_render(self):
        widget = JSONWidget()
        rendered = widget.render("json", {"spam": "eggs"})

        self.assertTrue("<textarea" in rendered)
        self.assertTrue('name="json"' in rendered)
        self.assertTrue("{\n  &quot;spam&quot;: &quot;eggs&quot;\n}" in rendered)
