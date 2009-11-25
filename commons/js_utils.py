# vim:fileencoding=utf8

# from commons.js_utils import simplejson を使ってください
try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        from django.utils import simplejson

class LazyEncoder(simplejson.JSONEncoder):
  def default(self, obj):
    from django.utils.functional import Promise
    if isinstance(obj, Promise):
      return force_unicode(obj)
    return obj

ESCAPEJS_JSON_STRING = (
    (u'<', u'\\u003c'),
    (u'>', u'\\u003e'),
    (u'&', u'\\u0026'),
)
def escapejs_json(s):
    """
    JSONEncoderエスケープされない文字を追加エスケープ
    """
    for c, code in ESCAPEJS_JSON_STRING:
        s = s.replace(c, code)
    return s

def force_js(value, type=None, encoder=None):
    """
    Changes a python value to javascript for use in templates
    """
    if type:
        if type.lower() == "bool":
            value = bool(value)
        elif type.lower() == "int":
            value = int(value)
        elif type.lower() == "string":
            value = str(value)
        elif type.lower() == "array":
            value = list(value)
  
    return simplejson.dumps(value, cls=(encoder or LazyEncoder))
