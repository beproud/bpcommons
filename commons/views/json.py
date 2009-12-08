# vim:fileencoding=utf-8
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from commons.utils.javascript import simplejson, escapejs_json

__all__ = (
    'make_simple_response',
    'make_simple_response400',
    'make_simple_response401',
    'make_simple_response403',
    'make_simple_response500',
)

def make_simple_response(status=200, msg=u'処理が成功しました', extra_context=None, content_type='text/plain'):
    obj = {'msg': msg}
    if extra_context:
        obj.update(extra_context)
    return HttpResponse(escapejs_json(simplejson.dumps(obj, cls=DjangoJSONEncoder)), status=str(status), content_type=content_type)

def make_simple_response400(msg=u'パラメータが不正です'):
    return make_simple_response(400, msg)

def make_simple_response401(msg=u'ログインしてください'):
    return make_simple_response(401, msg)

def make_simple_response403(msg=u'不正な処理です'):
    return make_simple_response(403, msg)

def make_simple_response500(msg=u'サーバー側で問題が発生しています。しばらく経ってからもう一度試してみてください'):
    return make_simple_response(500, msg)
