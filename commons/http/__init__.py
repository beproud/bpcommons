# vim:fileencoding=utf-8

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.encoding import iri_to_uri

from commons.utils.javascript import DjangoJSONEncoder
__all__ = (
    'JSONResponse',
    'HttpResponseNamedRedirect',
    'HttpResponseNamedPermanentRedirect',
)

class JSONResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data={}, status=200, content_type='application/json'):
        super(JSONResponse, self).__init__(simplejson.dumps(data, cls=DjangoJSONEncoder), status=status, content_type=content_type)

class HttpResponseNamedRedirect(HttpResponseRedirect):
    def __init__(self, lookup_view, *args, **kwargs):
        super(HttpResponseNamedRedirect, self).__init__(reverse(lookup_view, *args, **kwargs))

class HttpResponseNamedPermanentRedirect(HttpResponsePermanentRedirect):
    def __init__(self, lookup_view, *args, **kwargs):
        super(HttpResponseNamedPermanentRedirect, self).__init__(reverse(lookup_view, *args, **kwargs))
