import string
import re
import json

import six
from django.utils.encoding import force_str
from django.core.serializers.json import DjangoJSONEncoder
try:
    from django.utils.functional import keep_lazy  # Django-1.8 doesn't have it.
except ImportError:
    # allow_lazy has been deprecated at Django-1.10, will be removed at 2.0
    from django.utils.functional import allow_lazy as keep_lazy
    

# copy from beproud.utils.strutils.abbrev
def abbrev(s, num=255, end="..."):
    """
    文章を要約する
    返す文字列の長さは、num以上にならないのを保証します。

    >>> abbrev('spamspamspam', 6)
    'spa...'
    >>> abbrev('spamspamspam', 12)
    'spamspamspam'
    >>> abbrev('eggseggseggs', 1)
    'e'
    >>> abbrev('eggseggseggs', 2)
    'eg'
    >>> abbrev('eggseggseggs', 3)
    'egg'
    >>> abbrev('eggseggseggs', 4)
    'e...'
    >>> abbrev('eggseggseggs', 2, '.')
    'e.'
    """
    index = num - len(end)
    if len(s) > num:
        s = (s[:index] + end) if index > 0 else s[:num]
    return s


# copy from beproud.utils.html.urlize
def escape(html):
    """
    Returns the given HTML with ampersands, quotes and angle brackets encoded.
    """
    return (force_str(html).replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


# copy from beproud.utils.html.urlize
HTTP_SCHEME_RE = 'http[s]*'

# See: http://www.ietf.org/rfc/rfc1738.txt
URL_SAFE = "$-_.+"
URL_EXTRA = "!*'(),"
URL_PATH_RESERVED = ';?'
URL_QUERY_RESERVED = '#'
URL_OTHER_RESERVED = ':@&=/'
URL_RESERVED = URL_PATH_RESERVED + URL_QUERY_RESERVED + URL_OTHER_RESERVED
URL_ESCAPE = '%'
URL_ALNUM = string.ascii_letters + string.digits


URL_PATH_VALID_CHARS = URL_ALNUM + URL_SAFE + URL_EXTRA + URL_OTHER_RESERVED + URL_ESCAPE
URL_QUERY_VALID_CHARS = URL_ALNUM + URL_SAFE + URL_EXTRA + URL_OTHER_RESERVED + URL_PATH_RESERVED + URL_ESCAPE
URL_FRAGMENT_VALID_CHARS = URL_ALNUM + URL_SAFE + URL_EXTRA + URL_RESERVED + URL_ESCAPE


# 0-65535
# See: http://www.regular-expressions.info/numericranges.html
PORT_RE = "%s" % "|".join([
    "6553[0-5]",
    "655[0-2][0^9]",
    "65[0-4][0-9][0-9]",
    "6[0-4][0-9][0-9][0-9]",
    "[1-5][0-9][0-9][0-9][0-9]",
    "[1-9][0-9][0-9][0-9]",
    "[1-9][0-9][0-9]",
    "[1-9][0-9]",
    "[1-9]",
])

# See: http://www.shauninman.com/archive/2006/05/08/validating_domain_names
# See: http://www.iana.org/domains/root/db/
DOMAIN_RE = '(?:[a-z0-9](?:[-a-z0-9]*[a-z0-9])?\\.)+(?:(?:aero|arpa|a[cdefgilmnoqrstuwxz])|(?:cat|com|coop|b[abdefghijmnorstvwyz]|biz)|(?:c[acdfghiklmnorsuvxyz])|d[ejkmoz]|(?:edu|e[ceghrstu])|f[ijkmor]|(?:gov|g[abdefghilmnpqrstuwy])|h[kmnrtu]|(?:info|int|i[delmnoqrst])|(?:jobs|j[emop])|k[eghimnprwyz]|l[abcikrstuvy]|(?:mil|mobi|museum|m[acdghklmnopqrstuvwxyz])|(?:name|net|n[acefgilopruz])|(?:om|org)|(?:pro|p[aefghklmnrstwy])|qa|r[eouw]|s[abcdeghijklmnortvyz]|(?:travel|t[cdfghjklmnoprtvwz])|u[agkmsyz]|v[aceginu]|w[fs]|y[etu]|z[amw])'

# See: http://www.regular-expressions.info/regexbuddy/ipaccurate.html
IP_ADDRESS_RE = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

# Domain or IP address
IP_DOMAIN_RE = '(%s)|(%s)' % (DOMAIN_RE, IP_ADDRESS_RE)

# Domain or IP address with port number
URL_DOMAIN_RE = '(?:%s)(?::(%s))?' % (IP_DOMAIN_RE, PORT_RE)
URL_RE = r'(%s)\:\/\/(%s)(/[%s]*)?(?:\?([%s]*))?(?:\#([%s]*))?' % (
    HTTP_SCHEME_RE,
    URL_DOMAIN_RE,
    re.escape(URL_PATH_VALID_CHARS),
    re.escape(URL_QUERY_VALID_CHARS),
    re.escape(URL_FRAGMENT_VALID_CHARS),
)
URL_RE_CMP = re.compile(URL_RE)

URLIZE_TMPL = '<a href="%(link_url)s"%(attrs)s>%(link_text)s</a>'


# copy from beproud.utils.html.urlize
def urlize(text, trim_url_limit=None, attrs={}, url_re=URL_RE_CMP, autoescape=False):
    """text内URLを抽出してアンカータグで囲む

    URLのデリミタは半角カンマ、<>(エスケープ済み含む)、\s、全角スペース、行末で、これらが末尾にマッチしない場合はURLとして認識しません。
    URL部分は.+の最小マッチ、もしくはtrim_url_limitが指定された場合は{,trim_url_limit}の最小マッチとなります。

    -args

        text:           urlize対象文字列
        trim_url_limit: urlとして認識する文字数に上限を設ける場合は数値をセット
        nofollow:       Trueを与えるとタグにrel="nofollow"を付加
        autoescape:     Trueを与えるとタグエスケープを行います。

    """
    if autoescape:
        text = escape(text)

    def _repl(m):
        return URLIZE_TMPL % {
            "link_url": m.group(),
            "attrs": "".join(map(lambda x: ' %s="%s"' % x, attrs.items())),
            "link_text": (abbrev(m.group(), trim_url_limit)
                          if trim_url_limit is not None else m.group()),
        }

    return url_re.sub(_repl, text)


# copy from django.utils.html.strip_entities(). it was removed
def strip_entities(value):
    """Returns the given HTML with all entities (&something;) stripped."""
    return re.sub(r'&(?:\w+|#\d+);', '', force_text(value))
strip_entities = keep_lazy(strip_entities, six.text_type)


# copy from bputils: beproud.utils.javascript
JS_CONVERT_TYPES = {
    'bool': bool,
    'int': int,
    'string': str,
    'array': list,
}


# copy from bputils: beproud.utils.javascript
def force_js(value, typename=None, encoder=None):
    """
    Changes a python value to javascript for use in templates
    """
    if typename:
        typename = typename.lower()
        if typename in JS_CONVERT_TYPES:
            value = JS_CONVERT_TYPES[typename](value)
    return json.dumps(value, cls=(encoder or DjangoJSONEncoder))
