# vim:fileencoding=utf8
import base64

try:
	import cPickle as pickle
except ImportError:
	import pickle

from django.db import models

__all__ = (
    'BigIntegerField',
    'PositiveBigIntegerField',
    'PickledObjectField',
)

class BigIntegerField(models.IntegerField):
    empty_strings_allowed = False

    def get_internal_type(self):
        return "BigIntegerField"

    def db_type(self):
        return 'bigint' # Note this won't work with Oracle.

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
