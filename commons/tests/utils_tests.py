# vim:fileencoding=utf-8
from django.test import TestCase as DjangoTestCase

from commons.utils.strutils import * 
from commons.utils.javascript import *

class StringUtilsTestCase(DjangoTestCase):
    
    def test_trim(self):
        self.assertEqual(trim(u" テスト "), u"テスト")
        self.assertEqual(trim(u"テスト "), u"テスト")
        self.assertEqual(trim(u" テスト"), u"テスト")
        self.assertEqual(trim(u"　テスト　"), u"テスト")
        self.assertEqual(trim(u"テスト　"), u"テスト")
        self.assertEqual(trim(u"　テスト"), u"テスト")
        self.assertEqual(trim(u"　テスト "), u"テスト")

    def test_trim_none(self):
        self.assertEqual(trim(None), 'None')

    def test_force_int(self):
        self.assertEqual(force_int(192), 192)
        self.assertEqual(force_int("192"), 192)
        self.assertEqual(force_int("abc"), None)
        self.assertEqual(force_int("abc", "def"), "def")

    def test_force_int_none(self):
        self.assertEqual(force_int(None, 1), 1)
    
    def test_make_random_key(self):
        self.assertEqual(len(make_random_key(8)), 8)
        self.assertEqual(len(make_random_key(291)), 291)
        self.assertEqual(len(make_random_key(1)), 1)
    
    def test_make_random_key_empty(self):
        self.assertEqual(make_random_key(0), "")
        self.assertEqual(make_random_key(-1), "")

    def test_abbrev(self):
        self.assertEqual(abbrev('blahblahblah', 6), 'bla...')
        self.assertEqual(abbrev('blahblahblah', 12), 'blahblahblah')
        self.assertEqual(abbrev('blahblahblah', 11, '....'), 'blahbla....')
        self.assertEqual(abbrev('blahblahblah', 1), 'b')
        self.assertEqual(abbrev('blahblahblah', 2, '.'), 'b.')

    def test_abbrev_unicode(self):
        self.assertEqual(abbrev(u'テストテストテスト', 6), u'テスト...')
        self.assertEqual(abbrev(u'テストテストテスト', 9), u'テストテストテスト')
        self.assertEqual(abbrev(u'テストテストテスト', 8, '....'), u'テストテ....')
        self.assertEqual(abbrev(u'テストテストテスト', 1), u'テ')
        self.assertEqual(abbrev(u'テストテストテスト', 2, '.'), u'テ.')

class JavascriptUtilsTestCase(DjangoTestCase):

    def test_escapejs_json(self):
        self.assertEqual(escapejs_json(u"<テスト>"), u'\\u003cテスト\\u003e')
        self.assertEqual(escapejs_json(u"Q&A"), u"Q\\u0026A")
        self.assertEqual(escapejs_json(u"データ"), u"データ")

    def test_force_js(self):
        from datetime import datetime,date,time
        self.assertEqual(force_js({"msg": u"メッセージ"}), '{"msg": "\\u30e1\\u30c3\\u30bb\\u30fc\\u30b8"}')
        self.assertEqual(force_js(datetime(2009, 12, 22, 16, 35, 02)), '"2009-12-22 16:35:02"') 
        self.assertEqual(force_js(date(2009, 12, 22)), '"2009-12-22"') 
        self.assertEqual(force_js(time(16, 35, 02)), '"16:35:02"')

        # lazyオブジェクトテスト
        from django.utils.functional import lazy
        def test_func():
            return "value"
        lazy_test_func = lazy(test_func, str)
        val = lazy_test_func()
        self.assertEqual(force_js(val), '"value"')

    def test_force_js_type(self):
        self.assertEqual(force_js("", "bool"), "false")
        self.assertEqual(force_js("5", "int"), '5')
        self.assertEqual(force_js("test", "array"), '["t", "e", "s", "t"]')
        self.assertEqual(force_js(5, "string"), '"5"')
