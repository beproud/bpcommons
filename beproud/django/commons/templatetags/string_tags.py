#:coding=utf-8:
from __future__ import absolute_import

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text

from .compat import abbrev as abbrev_

register = template.Library()

def abbrev(val, num=20):
    return abbrev_(val, num)
abbrev = stringfilter(abbrev)
register.filter(abbrev)

def cat(value, arg): 
  """ 
  Concatenates value with argument 
  """ 
  return u"%s%s" % (value, force_text(arg))
cat.is_safe=True 
cat = stringfilter(cat)
register.filter(cat)
