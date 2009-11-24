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
