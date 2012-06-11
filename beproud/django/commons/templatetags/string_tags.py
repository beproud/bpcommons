#:coding=utf-8:

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode

register = template.Library()

def abbrev(val, num=20):
    from beproud.utils.strutils import abbrev
    return abbrev(val, num)
abbrev = stringfilter(abbrev)
register.filter(abbrev)

def cat(value, arg): 
  """ 
  Concatenates value with argument 
  """ 
  return u"%s%s" % (value, force_unicode(arg)) 
cat.is_safe=True 
cat = stringfilter(cat)
register.filter(cat)
