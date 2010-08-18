#:coding=utf-8:

from django.test import TestCase as DjangoTestCase

from django.forms import Form

from commons.forms import *

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
