# vim:fileencoding=utf8
from django.test import TestCase

__all__ = (
    'URLTestCase',
)

class BaseURLTestCase(type):
    def __new__(cls, name, bases, dict):
        counter = 0
        for url in dict['url_list']:
            def _url_test(self):
                response = self.client.get(url[0])
                self.assertEquals(response.status_code, url[1],
                        '%d != %d %s' % (response.status_code, url[1], url[0]))
            dict['test_url_%d' % counter] = _url_test
            counter += 1
        return type.__new__(cls, name, bases, dict)

class URLTestCase(TestCase):
    """
    URLに対してGETを実行してレスポンスを確認する
    """
    # TODO:ログインの対応
    # TODO:POSTの対応
    # TODO:パラメータの対応
    url_list = ()
