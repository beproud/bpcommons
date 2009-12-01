# vim:fileencoding=utf8
from django.db import models
from django.template import RequestContext
from django.shortcuts import render_to_response as django_render_to_response
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from commons.utils.javascript import simplejson, escapejs_json

def make_simple_response(status=200,msg=u'処理が成功しました',extra_context=None):
    obj = {'msg':msg}
    if extra_context :
        obj.update(extra_context)
    return HttpResponse(escapejs_json(simplejson.dumps(obj, cls=DjangoJSONEncoder)), status=str(status), mimetype='text/plain')

def make_simple_response401(msg=u'ログインしてください'):
    return HttpResponse(escapejs_json(simplejson.dumps({'msg':msg}, cls=DjangoJSONEncoder)), status=401, mimetype='text/plain')

def make_simple_response400(msg=u'パラメータが不正です'):
    return HttpResponse(escapejs_json(simplejson.dumps({'msg':msg}, cls=DjangoJSONEncoder)), status=400, mimetype='text/plain')

def make_simple_response403(msg=u'不正な処理です'):
    return HttpResponse(escapejs_json(simplejson.dumps({'msg':msg}, cls=DjangoJSONEncoder)), status=403, mimetype='text/plain')

def make_simple_response500(msg=u'サーバー側で問題が発生しています。しばらく経ってからもう一度試してみてください'):
    return HttpResponse(escapejs_json(simplejson.dumps({'msg':msg}, cls=DjangoJSONEncoder)), status=500, mimetype='text/plain')