# vim:fileencoding=utf8
try:
    import cPickle as pickle
except:
    import pickle
 
import base64

from django.db import models
from django.core import exceptions
from django.utils.encoding import smart_str

from oauth import oauth

class PickledObjectField(models.TextField):
    __metaclass__ = models.SubfieldBase
 
    def to_python(self, value):
        if value is None: return None
        if not isinstance(value, basestring): return value
        return pickle.loads(base64.b64decode(value))
 
    def get_db_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))

class BigIntegerField(models.IntegerField):
    empty_strings_allowed=False

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

class OAuthTokenField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 1024
        return super(OAuthTokenField,self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, oauth.OAuthToken):
            return value

        try:
            return oauth.OAuthToken.from_string(smart_str(value))
        except:
            raise exceptions.ValidationError("Invalid OAuth Token.")

    def get_db_prep_value(self, value):
        return smart_str(value)
