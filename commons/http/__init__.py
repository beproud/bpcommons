# vim:fileencoding=utf-8

from django.http import HttpResponse

from commons.utils.javascript import simplejson, DjangoJSONEncoder

__all__ = (
    'JsonResponse',
)

class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data={}, status=200, content_type='application/json'):
        super(JsonResponse, self).__init__(simplejson.dumps(data, cls=DjangoJSONEncoder), content_type=content_type)
