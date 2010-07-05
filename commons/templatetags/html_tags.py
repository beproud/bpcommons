# vim:fileencoding=utf8
import re

from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = Library()

def stripentities(value):
    """Strips all HTML entities"""
    from django.utils.html import strip_entities
    return strip_entities(value)
stripentities.is_safe = True
stripentities = stringfilter(stripentities)
register.filter(stripentities)

#def resolve_entities(value):
#    """Resolves HTML entities to unicode values"""
#    from commons.utils.html import resolve_entities
#    return resolve_entities(value)
#stripentities.is_safe = True
#stripentities = stringfilter(resolve_entities)
#register.filter(resolve_entities)

@register.filter
def to_anchor(text, autoescape=None):
    from bputils.html import urlize
    return mark_safe(urlize(text, attrs={"rel": "nofollow", "target": "_blank"}, autoescape=autoescape))
to_anchor.is_safe=True
to_anchor.needs_autoescape = True
to_anchor = stringfilter(to_anchor)

@register.filter
def to_anchortrunc(text, limit, autoescape=None):
    from bputils.html import urlize
    return mark_safe(urlize(text, attrs={"rel": "nofollow", "target": "_blank"}, 
                     trim_url_limit=limit, autoescape=autoescape))
to_anchortrunc.is_safe=True
to_anchortrunc.needs_autoescape = True
to_anchortrunc = stringfilter(to_anchortrunc)

@register.filter
def force_js(value, type=None):
    from bputils.javascript import force_js
    return mark_safe(force_js(value, type))
