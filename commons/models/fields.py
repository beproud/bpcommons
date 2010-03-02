# vim:fileencoding=utf8
import base64

try:
	import cPickle as pickle
except ImportError:
	import pickle

from django.utils import simplejson
from django.db import models

from commons.forms import JSONField as JSONFormField 
from commons.utils.javascript import DjangoJSONEncoder

__all__ = (
    'BigIntegerField',
    'PositiveBigIntegerField',
    'PickledObjectField',
    'JSONField',
)

try: 
    from django.db.models import BigIntegerField
except ImportError:
    from django.utils.translation import ugettext_lazy as _
    from django.conf import settings

    class BigIntegerField(IntegerField):
        empty_strings_allowed = False
        description = _("Big (8 byte) integer")
        MAX_BIGINT = 9223372036854775807
        def get_internal_type(self):
            return "BigIntegerField"

        def formfield(self, **kwargs):
            defaults = {'min_value': -BigIntegerField.MAX_BIGINT - 1,
                        'max_value': BigIntegerField.MAX_BIGINT}
            defaults.update(kwargs)
            return super(BigIntegerField, self).formfield(**defaults)

        def db_type(self):
            return 'NUMBER(19)' if settings.DATABASE_ENGINE == 'oracle' else 'bigint'

class PositiveBigIntegerField(BigIntegerField):
    def get_internal_type(self):
        return "PositiveBigIntegerField"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)

class PickledObjectField(models.TextField):
    __metaclass__ = models.SubfieldBase
 
    def to_python(self, value):
        if value is None: return None
        if not isinstance(value, basestring): return value
        return pickle.loads(base64.b64decode(value))
 
    def get_db_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))

class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase
 
    def formfield(self, **kwargs):
        return super(JSONField, self).formfield(form_class=JSONFormField, **kwargs)
 
    def to_python(self, value):
        if isinstance(value, basestring):
            value = simplejson.loads(value)
        return value
 
    def get_db_prep_save(self, value):
        if value is None: return
        return simplejson.dumps(data, cls=DjangoJSONEncoder)
 
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
