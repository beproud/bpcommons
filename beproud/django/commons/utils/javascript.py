# vim:fileencoding=utf-8

from django.utils.encoding import force_unicode
from django.utils import simplejson

from beproud.utils.javascript import escapejs_json, SafeJSONEncoder

__all__ = (
    'DjangoJSONEncoder',
)

class DjangoJSONEncoder(SafeJSONEncoder):
    def default(self, obj):
        try:
            #datetime対応
            return super(DjangoJSONEncoder, self).default(obj)
        except TypeError:
            # lazy翻訳オブジェクトなどの対応
            from django.utils.functional import Promise
            if isinstance(obj, Promise):
                return escapejs_json(force_unicode(obj))
            else:
                raise
