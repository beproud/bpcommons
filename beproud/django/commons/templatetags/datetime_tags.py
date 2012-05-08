# vim:fileencoding=utf-8

from django.template import Library

from beproud.django.commons.utils.timeutils import relative_time as rel_time

register = Library()

@register.filter
def relative_time(s):
    return rel_time(s) if s else ""
