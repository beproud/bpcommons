# vim:fileencoding=utf-8

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.encoding import iri_to_uri

from commons.utils.javascript import DjangoJSONEncoder
__all__ = (
    'JSONResponse',
    'HttpResponseReload',
    'HttpResponseNamedRedirect',
    'HttpResponseNamedPermanentRedirect',
)

class JSONResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data={}, status=200, content_type='application/json'):
        super(JSONResponse, self).__init__(simplejson.dumps(data, cls=DjangoJSONEncoder), content_type=content_type)

class HttpResponseReload(HttpResponse):
    """
    Reload page and stay on the same page from where request was made.

    example:

    def simple_view(request):
        if request.POST:
            form = CommentForm(request.POST):
            if form.is_valid():
                form.save()
                return HttpResponseReload(request)
        else:
            form = CommentForm()
        return render_to_response('some_template.html', {'form': form})
    """
    status_code = 302

    def __init__(self, request):
        HttpResponse.__init__(self)
        referer = request.META.get('HTTP_REFERER')
        self['Location'] = iri_to_uri(referer or "/")

class HttpResponseNamedRedirect(HttpResponseRedirect):
    def __init__(self, lookup_view, *args, **kwargs):
        super(HttpResponseNamedRedirect, self).__init__(reverse(lookup_view, *args, **kwargs))

class HttpResponseNamedPermanentRedirect(HttpResponsePermanentRedirect):
    def __init__(self, lookup_view, *args, **kwargs):
        super(HttpResponseNamedPermanentRedirect, self).__init__(reverse(lookup_view, *args, **kwargs))
