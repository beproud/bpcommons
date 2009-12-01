# vim:fileencoding=utf8
import re
from django.forms.fields import Field,RegexField,CharField,ChoiceField
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList, ValidationError

EMAIL_RE = re.compile(
        r"^[\w\.\-]+" # account
        r'@(?:[A-Z0-9]+(?:-*[A-Z0-9]+)*\.)+[A-Z]{2,6}$' # domain
    ,re.IGNORECASE
)
class EmailField(RegexField):
    default_error_messages = {
        'invalid': _(u'Eメールアドレスの形式が不正です'),
    }
    def __init__(self, *args, **kwargs):
        super(EmailField, self).__init__(EMAIL_RE, *args, **kwargs)

class PCEmailField(RegexField):
    default_error_messages = {
        'invalid': _(u'Eメールアドレスの形式が不正です')
    }
    def __init__(self, *args, **kwargs):
        super(PCEmailField, self).__init__(EMAIL_RE, *args, **kwargs)

    def clean(self, value):
        value = super(PCEmailField, self).clean(value)
        if value == u'':
            return value
        return value


alphanum_reg = re.compile(ur'^[a-zA-Z0-9\-_]*$')
class AlphaNumField(CharField):
    """ 半角英数字と"_","-"のみ許容するフィールド """
    default_error_messages = {
        'invalid': _(u'半角英数字で入力してください'),
    }
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        super(AlphaNumField, self).__init__(max_length,min_length,*args,
**kwargs)

    def clean(self, value):
        value = super(AlphaNumField, self).clean(value)
        if  value == u'':
            return value
        if not alphanum_reg.match(value):
            raise ValidationError(self.error_messages['invalid'])
        return value

num_reg = re.compile(ur'^[0-9]*$')
class NumCharField(CharField):
    """ 数字のみ許容する数値文字列フィールド """
    default_error_messages = {
        'invalid': _(u'数字で入力してください'),
    }
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        super(NumCharField, self).__init__(max_length,min_length,*args, **kwargs)

    def clean(self, value):
        value = super(NumCharField, self).clean(value)
        if  value == u'':
            return value
        if not num_reg.match(value):
            raise ValidationError(self.error_messages['invalid'])
        return value

class LazyChoiceField(ChoiceField):
    """ choicesを関数にできるChoiceField """
    def _get_choices(self):
        if callable(self._choices):
            return self._choices()
        return self._choices

    def _set_choices(self, value):
        self._choices = self.widget.choices = value

    choices = property(_get_choices, _set_choices)

# UTF-8のみ
class FullWidthCharField(RegexField):
    default_error_messages = {
        'invalid': _(u'全角文字を入力してください。'),
    }
    def __init__(self, *args, **kwargs):
        super(FullWidthCharField, self).__init__(
            re.compile(r"^[^ -~｡-ﾟ]*$"),
            *args,
            **kwargs
        )
