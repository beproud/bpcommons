# vim:fileencoding=utf-8

from django.core.serializers.json import DjangoJSONEncoder as BaseJSONEncoder

from django.utils.encoding import force_unicode

__all__ = (
    'DjangoJSONEncoder',
    'escapejs_json',
    'force_js',
)

from django.utils import simplejson

ESCAPEJS_JSON_STRING = (
    (u'<', u'\\u003c'),
    (u'>', u'\\u003e'),
    (u'&', u'\\u0026'),
)

JS_CONVERT_TYPES = {
    'bool': bool,
    'int': int,
    'string': str,
    'array': list,
}

class DjangoJSONEncoder(BaseJSONEncoder):
    def default(self, obj):
        try:
            #datetime対応
            return super(DjangoJSONEncoder, self).default(obj)
        except TypeError:
            # lazy翻訳オブジェクトなどの対応
            from django.utils.functional import Promise
            if isinstance(obj, Promise):
                return force_unicode(obj)
            else:
                raise

def escapejs_json(s):
    """
    JSONEncoderエスケープされない文字を追加エスケープ
    """
    for c, code in ESCAPEJS_JSON_STRING:
        s = s.replace(c, code)
    return s

def force_js(value, typename=None, encoder=None):
    """
    Changes a python value to javascript for use in templates
    """
    if typename:
        typename = typename.lower()
        if typename in JS_CONVERT_TYPES:
            value = JS_CONVERT_TYPES[typename](value)
    return simplejson.dumps(value, cls=(encoder or DjangoJSONEncoder))
