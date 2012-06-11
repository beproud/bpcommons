#:coding=utf-8:

from django.test import TestCase as DjangoTestCase
from django.utils import simplejson

from beproud.django.commons.utils.javascript import DjangoJSONEncoder

def dump_json(data):
    return simplejson.dumps(data, cls=DjangoJSONEncoder)

class DjangoJSONEncoderTestCase(DjangoTestCase):

    def test_escape(self):
        self.assertEqual(dump_json(u"<テスト>"), u'"\\u003c\\u30c6\\u30b9\\u30c8\\u003e"')
        self.assertEqual(dump_json(u"Q&A"), u'"Q\\u0026A"')
        self.assertEqual(dump_json(u"データ"), u'"\\u30c7\\u30fc\\u30bf"')

    def test_lazy(self):
        # lazyオブジェクトテスト
        from django.utils.functional import lazy
        def test_func():
            return "value"
        lazy_test_func = lazy(test_func, str)
        val = lazy_test_func()
        self.assertEqual(dump_json(val), '"value"')
