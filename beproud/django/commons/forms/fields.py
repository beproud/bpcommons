# vim:fileencoding=utf8
import re
from types import StringType, UnicodeType

from django.core import validators
from django.forms import CharField, RegexField, ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode 

from widgets import JSONWidget

__all__ = (
    'StripRegexField',
    'EmailField',
    'AlphaNumField',
    'NumCharField',
    'FullWidthCharField',
    'HiraganaCharField',
    'JSONField',
)

RE_EMAIL = re.compile(
    r"^[-\.!#$%&'*+/=?^_`{}|~0-9A-Z]+" # account
    r"@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}$" # domain
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

class JSONField(CharField):
    u""" JSONデータをポストする場合のフィールド。AJAXに便利かも """
    
    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = JSONWidget
        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        from django.utils import simplejson
        if value in validators.EMPTY_VALUES:
            return u''
        if isinstance(value, basestring):
            return smart_unicode(value)
        else:
            return simplejson.dumps(value)

    def clean(self, value):
        from django.utils import simplejson
        value = super(JSONField, self).clean(value)
        try:
            json_data = simplejson.loads(value)
        except Exception, e:
            raise ValidationError(self.error_messages['invalid'])
        return json_data
