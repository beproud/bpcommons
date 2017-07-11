# vim:fileencoding=utf-8

import re

from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlquote

__all__ = (
    'redirect_to',
    'http_response',
    'http_404',
    'http_500',
)

RE_QUOTE = re.compile(r"%([0-9A-Z]{1,2})")

def redirect_to(request, url, permanent=True, **kwargs):
    """
    A copy of the redirect_to view from django.views.generic.simple
    Copied since redirect_to doesn't work for urls that contain non-ascii
    keyword arguments.
    """
    if url is not None:
        klass = permanent and HttpResponsePermanentRedirect or HttpResponseRedirect
        quoted_kwargs = {}
        for k,v in kwargs.items():
            quoted_kwargs[k] = urlquote(v)

        # Encoded urls confuses python templating. Properly escape the templates.
        return klass(urlquote(RE_QUOTE.sub(r"%%\1", url) % quoted_kwargs))
    else:
        return HttpResponseGone()

def http_response(request, template, status=200):
    return HttpResponse(render_to_string(template, {'MEDIA_URL': settings.MEDIA_URL}), status=status)

def http_404(request, template='404.html'):
    return http_response(request, template, status=404)

def http_500(request, template='500.html'):
    return http_response(request, template, status=500)
