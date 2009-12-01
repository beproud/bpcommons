# vim:fileencoding=utf8
import re
import hashlib
from datetime import datetime,date,timedelta
from django.utils.hashcompat import md5_constructor
from django.conf import settings

def make_random_key(size=128):
    """
    """
    from random import sample
    keys = "" 
    src = [x for x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
    while True:
        diff = size - len(keys)
        if diff == 0 : break
        keys += "".join(sample(src,(diff < 20 and diff or 20)))
    return keys

_trim_re = re.compile(u'^[\s\u3000]+|[\s\u3000]+$')
def trim(s):
    """
    全角・半角も含めてトリミング
    """
    return _trim_re.sub(u'', s)

def abbrev(str, num=255, end="..."):
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
    index = num-len(end)
    if len(str) > num:
        str = (str[:index] + end) if index > 0 else str[:num] 
    return str
