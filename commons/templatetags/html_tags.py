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

url_re = re.compile(r'(http(s)?:\/\/[A-Za-z0-9%&=~?+-_/.#]+)')
@register.filter
def to_anchor(text):
    from django.utils.html import escape
    text = escape(text)
    text = url_re.sub(r'<a href="\1" target="_blank">\1</a>', text)
    return mark_safe(text.replace('\n', '<br />'))

@register.filter
def force_js(value, type=None):
    from commons.utils import force_js
    return mark_safe(force_js(value, type))