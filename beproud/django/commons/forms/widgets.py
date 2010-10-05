#:coding=utf8:

from django import forms
from django.utils import simplejson

from beproud.django.commons.utils.javascript import DjangoJSONEncoder

class JSONWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self.indent = kwargs.pop("indent", 2)
        super(JSONWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            value = simplejson.dumps(data, indent=self.indent, cls=DjangoJSONEncoder)
        return super(JSONWidget, self).render(name, value, attrs)
