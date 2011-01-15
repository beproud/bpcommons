# vim:fileencoding=utf-8

from django.http import HttpResponse
from django.utils import simplejson

from beproud.django.commons.utils.javascript import DjangoJSONEncoder

__all__ = (
    'JSONResponse',
)

class JSONResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data={}, status=200, content_type='application/json'):
        super(JSONResponse, self).__init__(simplejson.dumps(data, cls=DjangoJSONEncoder), status=status, content_type=content_type)

