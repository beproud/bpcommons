# vim:fileencoding=utf-8
import re

from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseGone
from django.utils.http import urlquote

__all__ = (
    'redirect_to',
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
        for k,v in kwargs.iteritems():
            quoted_kwargs[k] = urlquote(v)

        # Encoded urls confuses python templating. Properly escape the templates.
        return klass(urlquote(RE_QUOTE.sub(r"%%\1", url) % quoted_kwargs))
    else:
        return HttpResponseGone()
