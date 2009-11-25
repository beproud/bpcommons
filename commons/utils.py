# vim:fileencoding=utf8
from datetime import datetime,date,timedelta
from django.utils.hashcompat import md5_constructor
from django.template.defaultfilters import escapejs
from django.conf import settings
import hashlib

try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        from django.utils import simplejson

class Bag(object):
    def __init__(self, **kw):
        """Initialise, and set attributes from all keyword arguments."""
        self.__allow_access_to_unprotected_subobjects__=1
        self.__members=[]
        for k in kw.keys():
            setattr(self,k,kw[k])
            self.__remember(k)

    def __remember(self, k):
        """Add k to the list of explicitly set values."""
        if not k in self.__members:
            self.__members.append(k)

    def __getitem__(self, key):
        """Equivalent of dict access by key."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError, key

    def __setitem__(self, key, value):
        setattr(self, key, value)
        self.__remember(key)

    def has_key(self, key):
        return hasattr(self, key)

    def keys(self):
        return self.__members

    def iterkeys(self):
        return self.__members

    def __iter__(self):
        return iter(self.__members)

    def __str__(self):
        """Describe only those attributes explicitly set."""
        s = ""
        for x in self.__members:
            v = getattr(self, x)
            if s: s+=", "
            s += "%s: %s" % (x, `v`)
        return s

class LazyEncoder(simplejson.JSONEncoder):
  def default(self, obj):
    from django.utils.functional import Promise
    if isinstance(obj, Promise):
      return force_unicode(obj)
    return obj

def sha_hash(str, sha_method="512"):
    """
    """
    h = getattr(hashlib, "sha%s" % sha_method)()
    h.update((u"itto%sku" % str).encode('utf8')) # これはsoodaと同じである必要がある
    #h.update((u"al3xU%sba3" % str).encode('utf8')) # hash前に適当な文字列を加えている
    return h.hexdigest()

def make_random_key(size=128):
    """
    sizeで指定した長さのランダムなキーを生成
    利用される文字の範囲はa-zA-Z0-9
    """
    from random import sample
    keys = "" 
    src = [x for x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
    while True:
        diff = size - len(keys)
        if diff == 0 : break
        keys += "".join(sample(src,(diff < 20 and diff or 20)))
    return keys

def make_choices_and_dict(tuptup):
    choices = [(x[0],x[2]) for x in tuptup]
    const = dict([ (x[1],x[0]) for x in tuptup ])
    return choices, const

def make_choices_and_value(tuptup):
    values = dict([ (x[0],x[3]) for x in tuptup ])
    keys = dict([ (x[0],x[1]) for x in tuptup ])
    return make_choices_and_dict(tuptup) + (values, keys)

ESCAPEJS_JSON_STRING = (
    (u'<', u'\\u003c'),
    (u'>', u'\\u003e'),
    (u'&', u'\\u0026'),
)
def escapejs_json(s):
    """
    JSONEncoderエスケープされない文字を追加エスケープ
    """
    for c, code in ESCAPEJS_JSON_STRING:
        s = s.replace(c, code)
    return s

def force_js(value, type=None, encoder=None):
  """
  Changes a python value to javascript for use in templates
  """
  if type:
    if type.lower() == "bool":
      value = bool(value)
    elif type.lower() == "int":
      value = int(value)
    elif type.lower() == "string":
      value = str(value)
    elif type.lower() == "array":
      value = list(value)
  
  return simplejson.dumps(value, cls=(encoder or LazyEncoder))

def add_empty_tuple(tp ,add=("","--")):
    l = list(tp)
    l.insert(0,add)
    return tuple(l)

VALID_TAGS = {
    'b': (),
    'blockquote': ('style',),
    'em': (),
    'strong': (),
    'strike': (),
    'a': ('href', 'title'),
    'i': (),
    'br': (),
    'ul': (),
    'ol': (),
    'li': (),
    'u': (),
    'p': (),
    'h1': (),
    'h2': (),
    'h3': (),
    'h4': (),
    'table': (),
    'thead': (),
    'tbody': (),
    'tfoot': (),
    'th': (),
    'td': ('colspan',),
    'tr': ('rowspan',),
    'hr': (),
    'img': ('src', 'alt', 'title', 'width', 'height', 'align'),
    'span': ('style',),
    'div': ('style',),
    'font': ('size', 'style', 'color'),
}

VALID_STYLES = (
    "background-color",
    "color",
    "margin",
    "margin-left",
    "margin-right",
    "border",
    "padding",
    "font-weight",
    "font-style",
    "font-size",
    "text-align",
    "text-decoration",
)

def sanitize_html(htmlSource, encoding=None):
    """
    Clean bad html content. Currently this simply strips tags that
    are not in the VALID_TAGS setting.
    
    This function is used as a replacement for feedparser's _sanitizeHTML
    and fixes problems like unclosed tags and gives finer grained control
    over what attributes can appear in what tags.

    Returns the sanitized html content.
    """
    import re
    from BeautifulSoup import BeautifulSoup, Comment

    valid_styles = getattr(settings, "STRIPPER_VALID_STYLES", VALID_STYLES)
    valid_tags = getattr(settings, "STRIPPER_VALID_TAGS", VALID_TAGS)
    
    js_regex = re.compile(r'[\s]*(&#x.{1,7})?'.join(list('javascript')))
    css_regex = re.compile(r' *(%s): *([^;]*);?' % '|'.join(valid_styles), re.IGNORECASE)
    domain_regex = re.compile(r"^ *http\://(?!%s)" % re.escape(settings.DOMAIN)) 
    # Sanitize html with BeautifulSoup
    if encoding:
        soup = BeautifulSoup(htmlSource, fromEncoding=encoding)
    else:
        soup = BeautifulSoup(htmlSource)
    

    def entities(text):
        return text.replace('<','&lt;')\
                   .replace('>', '&gt;')\
                   .replace('"', '&quot;')\
                   .replace("'", '&apos;')
    
    # Sanitize html text by changing bad text to entities.
    # BeautifulSoup will do this for href and src attributes
    # on anchors and image tags but not for text.
    for text in soup.findAll(text=True):
        text.replaceWith(entities(text))
 
    # コメントを削る
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        else:
            tag.attrs = [(attr, js_regex.sub('', val))
                            for attr, val in tag.attrs 
                            if attr in valid_tags[tag.name]]

    
    # リンクに rel="nofollow"を追加
    
    for tag in soup.findAll("a", attrs={"href":domain_regex}):
        tag["rel"] = "nofollow" 

    # CSSを整理
    for tag in soup.findAll(attrs={"style":re.compile(".*")}):
        style = ""
        for key,val in css_regex.findall(tag["style"]):
            style += "%s:%s;" % (key,val.strip())
        tag["style"] = style

    return soup.renderContents().decode('utf8') 
