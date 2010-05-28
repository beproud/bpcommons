#:coding=utf8:

from django.test import TestCase as DjangoTestCase

from commons.test import URLTestCase

from commons.http import *

def test_json_response(request):
    return JSONResponse(data={"msg": u"成功しました"})

class JSONResponseTestCase(URLTestCase):
    url_list = (
        ('/test/json_response', {
            'check': ('assertOk', 'assertJson'),
        }),
    )
