# vim:fileencoding=utf8
from types import StringType, UnicodeType
from django.test import TestCase

__all__ = (
    'RequestTestCase',
    'URLTestCase',
)

class InvalidTest(Exception):
    def __init__(self, msg=''):
        self.msg = msg

    def __str__(self):
        return 'InvalidTest: %s' % self.msg

class RequestTestCase(TestCase):

    def assertStatus(self, response, status=200):
        self.assertEquals(response.status_code, status)

    def assertOk(self, response):
        self.assertStatus(response)

    def assertBadRequest(self, response):
        self.assertStatus(response, 400)

    def assertForbidden(self, response):
        self.assertStatus(response, 403)

    def assertNotFound(self, response):
        self.assertStatus(response, 404)

    def assertRedirect(self, response):
        self.assertStatus(response, 302)
        self._assertLocationHeader(response)

    def assertPermanentRedirect(self, response):
        self.assertStatus(response, 301)
        self._assertLocationHeader(response)

    def _assertLocationHeader(self, response):
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
        for data in dict['url_list']:
            # default
            url = ''
            check = ('assertOk',)
            method = 'get'
            username = ''
            password = ''
            urlparams = {}

            # url only
            if type(data) in (StringType, UnicodeType):
                url = data
            else:
                # url
                if len(data) < 0:
                    raise InvalidTest('"%s"' % data)
                url = data[0]
                # options
                if len(data) > 1:
                    options = data[1]
                    # check
                    if 'check' in options:
                        if type(options['check']) in (StringType, UnicodeType):
                            check = tuple(options['check'])
                        else:
                            check = options['check']
                    # method
                    if 'method' in options:
                        method = options['method']
                    # login
                    if 'username' in options:
                        username = options['username']
                    if 'password' in options:
                        password = options['password']
                    # urlparams
                    if 'urlparams' in options:
                        urlparams = options['urlparams']

            def _outer(url, check, method, username, password, urlparams):
                def _url_test(self):
                    if username:
                        self.assertTrue(self.client.login(username=username, password=password))
                    response = getattr(self.client, method)(url, urlparams)
                    for check_options in check:
                        # check method
                        if type(check_options) in (StringType, UnicodeType):
                            getattr(self, check_options)(response)
                        else:
                            _method = getattr(self, check_options[0])
                            if len(check_options) > 1:
                                args = check_options[1]
                                if len(check_options) > 2:
                                    kwargs = check_options[2]
                                    _method(response, *args, **kwargs)
                                else:
                                    _method(response, *args)
                            else:
                                _method(response)
                return _url_test

            dict['test_url_%d' % counter] = _outer(url, check, method, username, password, urlparams)
            counter += 1
        return type.__new__(cls, name, bases, dict)

class URLTestCase(RequestTestCase):
    """
    URLに対してGET/POSTを実行してレスポンスを確認する

    url_list = (
        ('/foo/bar', {
            'check': ('assertOk', ('assertJson', [], {})),
            'method': 'post',
            'urlparams': {'param1': 'value1',
            'username': 'user1',
            'password': 'pass1'}
        }),
        r'/',
    )
    """
    url_list = ()
    __metaclass__ = BaseURLTestCase
