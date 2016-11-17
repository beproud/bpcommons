#:coding=utf-8:

from django.http import JsonResponse

__all__ = (
        'get_object_or_None',
        'make_simple_response',
        'make_simple_response400',
        'make_simple_response401',
        'make_simple_response403',
        'make_simple_response500',
)

def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    from django.shortcuts import _get_queryset
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

def make_simple_response(msg=u'処理が成功しました', extra_context=None, status=200, content_type='application/json'):
    obj = {'msg': msg}
    if extra_context:
        obj.update(extra_context)
    return JsonResponse(obj, status=status, content_type=content_type)

def make_simple_response400(msg=u'パラメータが不正です'):
    return make_simple_response(msg, status=400)

def make_simple_response401(msg=u'ログインしてください'):
    return make_simple_response(msg, status=401)

def make_simple_response403(msg=u'不正な処理です'):
    return make_simple_response(msg, status=403)

def make_simple_response500(msg=u'サーバー側で問題が発生しています。しばらく経ってからもう一度試してみてください'):
    return make_simple_response(msg, status=500)
