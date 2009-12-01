# vim:fileencoding=utf8
from django.db import models
from django.template import RequestContext
from django.shortcuts import render_to_response as django_render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils import simplejson
from django.utils.http import urlquote
from django.core.serializers.json import DjangoJSONEncoder
from commons.utils import escapejs_json

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

def redirect_to(request, url, permanent=True, **kwargs):
    """
    A copy of the redirect_to view from django.views.generic.simple
    Copied since redirect_to doesn't work for urls that contain non-ascii 
    keyword arguments.
    """
    import re

    if url is not None:
        klass = permanent and HttpResponsePermanentRedirect or HttpResponseRedirect
        quoted_kwargs = {}
        for k,v in kwargs.iteritems():
            quoted_kwargs[k] = urlquote(v)

        # Encoded urls confuses python templating. Properly escape the templates.
        return klass(urlquote(re.sub(r"%([0-9A-Z]{1,2})", r"%%\1", url) % quoted_kwargs))
    else:
        return HttpResponseGone()
