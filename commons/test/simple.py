# vim:fileencoding=utf8
from django.test import TestCase

__all__ = (
    'RequestTestCase',
    'URLTestCase',
)

class RequestTestCase(TestCase):

    def assertStatus(self, response, status=200):
        self.assertEquals(response.status_code, status)

    def assertStatusOk(self, response):
        self.assertStatus(response)

    def assertStatusBadRequest(self, response):
        self.assertStatus(response, 400)

    def assertStatusForbidden(self, response):
        self.assertStatus(response, 403)

    def assertStatusNotFound(self, response):
        self.assertStatus(response, 404)

    def assertRedirect(self, response):
        self.assertStatus(response, 302)
        self._assertLocationHeader(response)

    def assertPermanentRedirect(self, response):
        self.assertStatus(response, 301)
        self._assertLocationHeader(response)

    def _assertLocationHeader(self, response)
        self.assertTrue(response.get("Location") is not None)

    def assertNotAllowed(self, response, allow=None):
        self.assertEquals(response.status_code, 405)
        if allow is not None:
            self.assertEquals(response["Allow"], allow)

    def assertGone(self, response):
        self.assertEquals(response.status_code, 410)

    def assertHtml(self, response):
        self.assertContains(response, "<html") # open tag
        self.assertContains(response, "</html>") # close tag
        self.assertContains(response, "<head")
        self.assertContains(response, "</head>")
        self.assertContains(response, "<body")
        self.assertContains(response, "</body>")

    def assertJson(self, response):
        try:
            return simplejson.loads(response.content)
        except ValueError,e:
            self.fail(e.message)

    def assertXml(self, response):
        from xml.parsers import expat
        try:
            p = expat.ParserCreate() 
            return p.Parse(response.content)
        except expat.ExpatError, e:
            self.fail(e.message)

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

class URLTestCase(RequestTestCase):
    """
    URLに対してGETを実行してレスポンスを確認する
    """
    # TODO:ログインの対応
    # TODO:POSTの対応
    # TODO:パラメータの対応
    url_list = ()
