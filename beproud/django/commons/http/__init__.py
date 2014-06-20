# vim:fileencoding=utf-8

try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse

from beproud.django.commons.utils.javascript import DjangoJSONEncoder

__all__ = (
    'JSONResponse',
)


class JSONResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data={}, status=200, content_type='application/json'):
        super(JSONResponse, self).__init__(
            json.dumps(data, cls=DjangoJSONEncoder),
            status=status,
            content_type=content_type,
        )
