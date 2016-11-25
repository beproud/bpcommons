#:coding=utf-8:

import pytest
from django.test import TestCase as DjangoTestCase

from beproud.django.commons.shortcuts import get_object_or_None, make_simple_response


@pytest.mark.django_db
class TestGetObjectOrNone(object):

    @pytest.fixture
    def target(self):
        from shortcuts_app.models import ShortcutModel
        return ShortcutModel

    def test_simple(self, target):
        instance = target.objects.create(name='test')
        obj = get_object_or_None(target, pk=instance.pk)
        assert obj is not None

    def test_queryset(self, target):
        i1 = target.objects.create(name='queryset')
        i2 = target.objects.create(name='queryset')
        i3 = target.objects.create(name='queryset')

        qs = target.objects.filter(name="queryset")
        obj = get_object_or_None(qs, pk=i2.pk)
        assert obj is not None

    def test_none(self, target):
        i1 = target.objects.create(name='test')
        i2 = target.objects.create(name='test')
        pk = max(i1.pk, i2.pk) + 1

        obj = get_object_or_None(target, pk=pk)
        assert obj is None


class MakeSimpleResponseTestCase(DjangoTestCase):

    def test_simple(self):
        response = make_simple_response()
        self.assertEqual(
            response.content,
            u'{"msg": "\\u51e6\\u7406\\u304c\\u6210\\u529f\\u3057\\u307e\\u3057\\u305f"}',
        )
