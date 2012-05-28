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
            value = simplejson.dumps(value, indent=self.indent, cls=DjangoJSONEncoder)
        return super(JSONWidget, self).render(name, value, attrs)

class AdminJSONWidget(JSONWidget):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'vLargeTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminJSONWidget, self).__init__(attrs=final_attrs)