#:coding=utf-8:

import re
from six import text_type

try:
    import json
except ImportError:
    import simplejson as json

from django.forms import RegexField
from django.utils.translation import gettext_lazy as _

__all__ = (
    'StripRegexField',
    'EmailField',
    'AlphaNumField',
    'NumCharField',
    'FullWidthCharField',
    'HiraganaCharField',
)

RE_EMAIL = re.compile(
    r"^[-\.!#$%&'*+/=?^_`{}|~0-9A-Z]+"  # account
    r"@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+(xn--[A-Z0-9\-]+|[A-Z]{2,15})$",  # domain
    re.IGNORECASE
)
RE_ALPHA_NUM = re.compile(r'^[a-zA-Z0-9\-_]*$')
RE_NUM = re.compile(r'^[0-9]*$')
RE_FULL_WIDTH = re.compile(u'[一-龠]+|[ぁ-ん]+|[ァ-ヴ]+|[０-９]+')
RE_HIRAGANA = re.compile(u'^[ぁ-ゞー〜～＆ 　、・]*$')


class StripRegexField(RegexField):
    """
    検証する前にstripする正規表現のフィールド
    """
    def clean(self, value):
        if isinstance(value, text_type):
            value = value.strip()
        return super(StripRegexField, self).clean(value)


class EmailField(StripRegexField):
    default_error_messages = {
        'invalid': _(u'Eメールアドレスの形式が不正です'),
    }

    def __init__(self, *args, **kwargs):
        super(EmailField, self).__init__(RE_EMAIL, *args, **kwargs)


class AlphaNumField(StripRegexField):
    """
    半角英数字と"_","-"のみ許容するフィールド
    """
    default_error_messages = {
        'invalid': _(u'半角英数字で入力してください'),
    }

    def __init__(self, *args, **kwargs):
        super(AlphaNumField, self).__init__(RE_ALPHA_NUM, *args, **kwargs)


class NumCharField(StripRegexField):
    """
    数字のみを許容するフィールド
    """
    default_error_messages = {
        'invalid': _(u'数字で入力してください'),
    }

    def __init__(self, *args, **kwargs):
        super(NumCharField, self).__init__(RE_NUM, *args, **kwargs)


class FullWidthCharField(StripRegexField):
    """
    全角文字のみを許容するフィールド
    """
    default_error_messages = {
        'invalid': _(u'全角文字を入力してください。'),
    }

    def __init__(self, *args, **kwargs):
        super(FullWidthCharField, self).__init__(RE_FULL_WIDTH, *args, **kwargs)


class HiraganaCharField(StripRegexField):
    u"""
    全角ひらがなのみ許容するフィールド
    """
    default_error_messages = {
        'invalid': _(u'ひらがなで入力してください'),
    }

    def __init__(self, *args, **kwargs):
        super(HiraganaCharField, self).__init__(RE_HIRAGANA, *args, **kwargs)
