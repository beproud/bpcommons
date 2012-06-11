#:coding=utf-8:

from beproud.django.commons.test import URLTestCase

from beproud.django.commons.http import *

def test_json_response(request):
    return JSONResponse(data={"msg": u"成功しました"})

class JSONResponseTestCase(URLTestCase):
    url_list = (
        ('/test/json_response', {
            'check': ('assertOk', 'assertJson'),
        }),
    )
