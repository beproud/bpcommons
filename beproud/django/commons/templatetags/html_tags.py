#:coding=utf-8:
from __future__ import absolute_import

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from .compat import urlize, strip_entities, force_js as force_js_

register = Library()

def stripentities(value):
    """Strips all HTML entities"""
    return strip_entities(value)
stripentities.is_safe = True
stripentities = stringfilter(stripentities)
register.filter(stripentities)

@register.filter
def to_anchor(text, autoescape=None):
    return mark_safe(urlize(text, attrs={"rel": "nofollow", "target": "_blank"}, autoescape=autoescape))
to_anchor.is_safe=True
to_anchor.needs_autoescape = True
to_anchor = stringfilter(to_anchor)

@register.filter
def to_anchortrunc(text, limit, autoescape=None):
    return mark_safe(urlize(text, attrs={"rel": "nofollow", "target": "_blank"},
                     trim_url_limit=limit, autoescape=autoescape))
to_anchortrunc.is_safe=True
to_anchortrunc.needs_autoescape = True
to_anchortrunc = stringfilter(to_anchortrunc)

@register.filter
def force_js(value, type=None):
    return mark_safe(force_js_(value, type))
