# vim:fileencoding=utf-8
import re
from random import sample

RE_TRIM = re.compile(u'^[\s\u3000]+|[\s\u3000]+$')

def trim(s):
    """
    全角・半角も含めてトリミング
    """
    from django.utils.encoding import force_unicode
    return RE_TRIM.sub(u'', force_unicode(s))

def force_int(num, default=None):
    try:
        return int(num)
    except:
        return default

def make_random_key(size=128):
    keys = ""
    src = [x for x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
    while True:
        diff = size - len(keys)
        if diff <= 0:
            break
        keys += "".join(sample(src, (diff < 20 and diff or 20)))
    return keys

def abbrev(s, num=255, end="..."):
    """
    文章を要約する
    質問の文章などで利用

    返す文字列の長さは、num以上にならないのを保証します。

    >>> abbrev('blahblahblah', 6)
    'bla...'
    >>> abbrev('blahblahblah', 12)
    'blahblahblah'
    >>> abbrev('blahblahblah', 13)
    'blahblahb...'
    >>> abbrev('blahblahblah', 1)
    'b'
    >>> abbrev('blahblahblah', 2, '.')
    'b.'
    """
    index = num - len(end)
    if len(s) > num:
        s = (s[:index] + end) if index > 0 else s[:num]
    return s
