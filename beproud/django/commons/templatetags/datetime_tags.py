# vim:fileencoding=utf-8
from django.template import Library

from beproud.django.commons.utils.timeutils import relative_time

register = Library()

@register.filter
def relative_time(s):
    return relative_time(s) if s else ""
