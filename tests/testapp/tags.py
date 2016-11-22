#:coding=utf-8:

from django.template import Library

from beproud.django.commons.utils.template import data_template_tag 
register = Library()

@register.tag
@data_template_tag
def get_my_data(num):
    if num == 121:
        return "MY DATA"
    else:
        return "ERROR"

@register.tag
@data_template_tag
def get_my_kwarg_data(num, status=None, other="other"):
    return "%s:%s:%s" % (num, status, other)
