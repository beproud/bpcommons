# vim:fileencoding=utf8
import types
import re
import urlparse
import urllib
import cgi
from datetime import date,datetime,timedelta
from django import template
from time import strptime
from django.utils.html import escape
from django.template import Library, Node, NodeList, Variable, TemplateSyntaxError,VariableDoesNotExist
from django.template.defaulttags import URLNode
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse as url_reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe,SafeUnicode
from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms
register = Library()

@register.filter
@stringfilter
def abbrev(val, num=20):
    ret = val
    if len(val) > num:
        ret = val[0:num] + "..."
    return ret

def cat(value, arg): 
  """ 
  Concatenates value with argument 
  """ 
  return u"%s%s" % (value, force_unicode(arg)) 
cat.is_safe=True 
cat = stringfilter(cat)
register.filter(cat)

class AbbrevBlockNode(template.Node):
    """
    A node whos output is truncated to the number of characters given.
    """
    def __init__(self, nodelist, max_length):
        self.nodelist = nodelist
        self.max_length = template.Variable(max_length)

    def render(self, context):
        try:
            max_length = self.max_length.resolve(context)
            text = self.nodelist.render(context)
            return abbrev(text, max_length)
        except template.VariableDoesNotExist:
            return ''

@register.tag(name="abbrev")
def do_abbrev(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument" % bits[0])
    max_length = bits[1]
    nodelist = parser.parse(('end%s' % bits[0],))
    parser.delete_first_token()
    return AbbrevBlockNode(nodelist, max_length)
