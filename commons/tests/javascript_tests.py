#:coding=utf8:

from django.test import TestCase as DjangoTestCase

from commons.utils.javascript import DjangoJSONEncoder
from bputils import simplejson

def dump_json(data):
    return simplejson.dumps(data, cls=DjangoJSONEncoder)

class DjangoJSONEncoderTestCase(DjangoTestCase):


    def test_escape(self):
        self.assertEqual(dump_json(u"<テスト>"), u'"\\u003c\\u30c6\\u30b9\\u30c8\\u003e"')
        self.assertEqual(dump_json(u"Q&A"), u'"Q\\u0026A"')
        self.assertEqual(dump_json(u"データ"), u'"\\u30c7\\u30fc\\u30bf"')

    def test_datetime(self):
        from datetime import datetime,date,time
        self.assertEqual(dump_json({"msg": u"メッセージ"}), '{"msg": "\\u30e1\\u30c3\\u30bb\\u30fc\\u30b8"}')
        self.assertEqual(dump_json(datetime(2009, 12, 22, 16, 35, 02)), '"2009-12-22 16:35:02"') 
        self.assertEqual(dump_json(date(2009, 12, 22)), '"2009-12-22"') 
        self.assertEqual(dump_json(time(16, 35, 02)), '"16:35:02"')

    def test_lazy(self):
        # lazyオブジェクトテスト
        from django.utils.functional import lazy
        def test_func():
            return "value"
        lazy_test_func = lazy(test_func, str)
        val = lazy_test_func()
        self.assertEqual(dump_json(val), '"value"')

    def test_decimal(self):
        from decimal import Decimal
        self.assertEqual(dump_json(Decimal("5")), '5')
        self.assertEqual(dump_json({"dec": Decimal("8.12")}), '{"dec": 8.12}')
