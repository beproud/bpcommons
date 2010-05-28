#:coding=utf8:

from django.test import TestCase as DjangoTestCase

from commons.shortcuts import *

from commons.tests.shortcuts.shortcuts_app.models import ShortcutModel

class GetObjectOrNoneTestCase(DjangoTestCase):

    def test_simple(self):
        obj = get_object_or_None(ShortcutModel, pk=1)
        self.assertTrue(obj is not None)

    def test_queryset(self):
        qs = ShortcutModel.objects.filter(name="queryset")
        obj = get_object_or_None(qs, pk=2)
        self.assertTrue(obj is not None)

    def test_none(self):
        obj = get_object_or_None(ShortcutModel, pk=5)
        self.assertTrue(obj is None)
