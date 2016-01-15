#:coding=utf-8:

from django.test import TestCase as DjangoTestCase

from beproud.django.commons.shortcuts import get_object_or_None, make_simple_response


class GetObjectOrNoneTestCase(DjangoTestCase):

    def _getTarget(self):
        from beproud.django.commons.tests.test_shortcuts.shortcuts_app.models import ShortcutModel
        return ShortcutModel

    def test_simple(self):
        target = self._getTarget()
        obj = get_object_or_None(target, pk=1)
        self.assertTrue(obj is not None)

    def test_queryset(self):
        target = self._getTarget()
        qs = target.objects.filter(name="queryset")
        obj = get_object_or_None(qs, pk=2)
        self.assertTrue(obj is not None)

    def test_none(self):
        target = self._getTarget()
        obj = get_object_or_None(target, pk=5)
        self.assertTrue(obj is None)


class MakeSimpleResponseTestCase(DjangoTestCase):

    def test_simple(self):
        response = make_simple_response()
        self.assertEqual(
            response.content,
            u'{"msg": "\\u51e6\\u7406\\u304c\\u6210\\u529f\\u3057\\u307e\\u3057\\u305f"}',
        )
