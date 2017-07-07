#:coding=utf-8:

try:
    import json
except ImportError:
    import simplejson as json

from six import string_types, with_metaclass
from django.test import TestCase

__all__ = (
    'InvalidTest',
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

    def assertCreated(self, response):
        self.assertStatus(response, 201)

    def assertAccepted(self, response):
        self.assertStatus(response, 202)

    def assertNonAuthoritativeInfo(self, response):
        self.assertStatus(response, 203)

    def assertNoContent(self, response):
        self.assertStatus(response, 204)

    def assertResetContent(self, response):
        self.assertStatus(response, 205)

    def assertPartialContent(self, response):
        self.assertStatus(response, 206)

    def assertMultipleChoices(self, response):
        self.assertStatus(response, 300)

    def assertPermanentRedirect(self, response, redirect_url=None):
        self.assertStatus(response, 301)
        self._assertLocationHeader(response, redirect_url)

    def assertRedirect(self, response, redirect_url=None):
        self.assertStatus(response, 302)
        self._assertLocationHeader(response, redirect_url)

    def assertBadRequest(self, response):
        self.assertStatus(response, 400)

    def assertForbidden(self, response):
        self.assertStatus(response, 403)

    def assertNotFound(self, response):
        self.assertStatus(response, 404)

    def assertNotAllowed(self, response, allow=None):
        self.assertEquals(response.status_code, 405)
        if allow is not None:
            self.assertEquals(response["Allow"], allow)

    def assertGone(self, response):
        self.assertEquals(response.status_code, 410)

    def assertHtml(self, response):
        self.assertContains(response, "<html")  # open tag
        self.assertContains(response, "</html>")  # close tag
        self.assertContains(response, "<head")
        self.assertContains(response, "</head>")
        self.assertContains(response, "<body")
        self.assertContains(response, "</body>")

    def assertJson(self, response):
        try:
            return json.loads(response.content)
        except ValueError as e:
            self.fail(e.message)

    def assertXml(self, response):
        from xml.parsers import expat
        try:
            p = expat.ParserCreate()
            return p.Parse(response.content)
        except expat.ExpatError as e:
            self.fail(e.message)

    def _assertLocationHeader(self, response, redirect_url=None):
        if redirect_url is None:
            self.assertTrue(response.get("Location", None) is not None)
        else:
            self.assertEquals(response.get("Location", None), redirect_url)


class BaseURLTestCase(type):
    def __new__(cls, name, bases, attrs):
        counter = 0
        _username = attrs.get('username')
        _password = attrs.get('password')
        for data in attrs['url_list']:
            # default
            name = ''
            url = ''
            headers = {}
            check = ('assertOk',)
            method = 'get'
            username = _username
            password = _password
            urlparams = {}

            # url only
            if isinstance(data, string_types):
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
                        if isinstance(options['check'], string_types):
                            check = (options['check'], )
                        else:
                            check = options['check']
                    # name
                    if 'name' in options:
                        name = '_%s' % options['name']
                    if 'headers' in options:
                        headers = options['headers']
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

            def _outer(url, check, method, headers, username, password, urlparams):
                def _url_test(self):
                    if username:
                        self.assertTrue(self.client.login(username=username, password=password))
                    response = getattr(self.client, method)(url, urlparams, **headers)
                    for check_options in check:
                        # check method
                        if isinstance(check_options, string_types):
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

            attrs['test_url_%d%s' % (counter, name)] = _outer(url, check, method, headers, username, password, urlparams)
            counter += 1
        return type.__new__(cls, name, bases, attrs)


class URLTestCase(with_metaclass(BaseURLTestCase, RequestTestCase)):
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
    username = ''
    password = ''
    url_list = ()
