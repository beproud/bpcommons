# vim:fileencoding=utf8
import re
from types import StringType, UnicodeType

from django.forms import CharField, RegexField, ValidationError
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'StripRegexField',
    'EmailField',
    'AlphaNumField',
    'NumCharField',
    'FullWidthCharField',
)

RE_EMAIL = re.compile(
    r'^[\w\.\-]+' # account
    r'@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}$' # domain
    , re.IGNORECASE
)
RE_ALPHA_NUM = re.compile(ur'^[a-zA-Z0-9\-_]*$')
RE_NUM = re.compile(ur'^[0-9]*$')
RE_FULL_WIDTH = re.compile(ur'[一-龠]+|[ぁ-ん]+|[ァ-ヴ]+|[０-９]+')
RE_HIRAGANA = re.compile(ur'^[ぁ-ゞー〜～＆ 　、・]*$')

class StripRegexField(RegexField):
    """
    検証する前にstripする正規表現のフィールド
    """
    def clean(self, value):
        if type(value) in (StringType, UnicodeType):
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

class JsonField(CharField):
    u""" JSONデータをポストする場合のフィールド。AJAXに便利かも """
    
    def __init__(self, *args, **kwargs):
        super(JsonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        from django.utils import simplejson
        value = super(JsonField, self).clean(value)
        try:
            json_data = simplejson.loads(value)
        except Exception, e:
            raise ValidationError(self.error_messages['invalid'])
        return json_data
