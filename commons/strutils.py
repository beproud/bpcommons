# vim:fileencoding=utf8
import re
import hashlib
from datetime import datetime,date,timedelta
from django.utils.hashcompat import md5_constructor
from django.template.defaultfilters import escapejs
from django.conf import settings
from django.utils.safestring import SafeData, mark_safe
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.utils.http import urlquote
from django.utils.html import escape

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

anchor_re_str = ur'(http[s]*\:\/\/.%s)(,|&gt;|&lt;|<|>|\s| |　|\xe3\x80\x80|$)'
anchor_re_nolimit = re.compile(anchor_re_str % "+?")
anchor_re_res_str = ur'<a href="\1"%s>\1</a>\2'
def urlize(text, trim_url_limit=None, nofollow=False, autoescape=False):
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

    if trim_url_limit:
        anchor_re = re.compile(anchor_re_str % "{,%s}?" % trim_url_limit)
    else:
        anchor_re = anchor_re_nolimit

    if nofollow:
        anchor_re_result = anchor_re_res_str % ' rel="nofollow"'
    else:
        anchor_re_result = anchor_re_res_str % ""

    return anchor_re.sub(anchor_re_result, text)


