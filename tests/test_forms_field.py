#:coding=utf-8:

from django.test import TestCase as DjangoTestCase

from django.forms import Form

from beproud.django.commons.forms import EmailField

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

    def test_longtld(self):
        form = EmailTestForm({"email": "spam@eggs.engineer"})
        self.assertTrue(form.is_valid())

    def test_punycode(self):
        form = EmailTestForm({"email": "spam@eggs.xn--i1b6b1a6a2e"})
        self.assertTrue(form.is_valid())


