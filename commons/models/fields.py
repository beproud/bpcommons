# vim:fileencoding=utf8
import base64

try:
	import cPickle as pickle
except ImportError:
	import pickle

from django import VERSION as DJANGO_VERSION
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.db import load_backend
from django.db import connection
from django.db import models
from django.conf import settings

from commons.forms import JSONField as JSONFormField 
from commons.utils.javascript import DjangoJSONEncoder

__all__ = (
    'BigIntegerField',
    'PositiveBigIntegerField',
    'BigAutoField',
    'BigForeignKey',
    'PickledObjectField',
    'JSONField',
)

if DJANGO_VERSION > (1,2):
    from django.db.models import BigIntegerField

    class BigAutoField(models.AutoField):
        description = _("Big (8 byte) integer")
     
        CREATION_DATA = {
            'django.db.backends.mysql': "bigint AUTO_INCREMENT",
            'django.db.backends.oracle': "NUMBER(19)",
            'django.db.backends.postgresql': "bigserial",
            'django.db.backends.postgresql_psycopg2': "bigserial",
            'django.db.backends.sqlite3': "integer", # Not a bigint!!!
        }

        def db_type(self, connection):
            try:
                for backend, db_type in self.CREATION_DATA.items():
                    try:
                        module = load_backend(backend)
                        if isinstance(connection, getattr(module, 'DatabaseWrapper')):
                            return db_type
                    except (ImportError, exceptions.ImproperlyConfigured):
                        pass
            except (KeyError, AttributeError):
                pass
            raise exceptions.ImproperlyConfigured("BigAutoField does not support the %s database backend" % connection.settings_dict["ENGINE"])

        def get_internal_type(self):
            return "BigAutoField"
        
        def get_prep_value(self, value):
            if value is None:
                return None
            return long(value)
        
        def to_python(self, value):
            if value is None:
                return value
            try:
                return long(value)
            except (TypeError, ValueError):
                raise exceptions.ValidationError(self.error_messages['invalid'])

    class BigForeignKey(models.ForeignKey):
        
        def db_type(self, connection):
            # The database column type of a ForeignKey is the column type
            # of the field to which it points. An exception is if the ForeignKey
            # points to an AutoField/PositiveIntegerField/PositiveSmallIntegerField,
            # in which case the column type is simply that of an IntegerField.
            # If the database needs similar types for key fields however, the only
            # thing we can do is making AutoField an IntegerField.
            rel_field = self.rel.get_related_field()
            if (isinstance(rel_field, models.AutoField) or
                    (not connection.features.related_fields_match_type and
                    isinstance(rel_field, (PositiveBigIntegerField,
                                           models.PositiveIntegerField,
                                           models.PositiveSmallIntegerField)))):
                return BigIntegerField().db_type(connection=connection)
            return rel_field.db_type(connection=connection)
else:
    """
    For Django 1.1
    """
    from django.utils.translation import ugettext_lazy as _

    class BigIntegerField(models.IntegerField):
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
            try:
                module = load_backend("oracle")
                if isinstance(connection, getattr(module, 'DatabaseWrapper')):
                    return 'NUMBER(19)'
            except (KeyError, AttributeError, ImportError, exceptions.ImproperlyConfigured):
                pass
            return 'bigint'

    class BigAutoField(models.AutoField):
        
        CREATION_DATA = {
            'mysql': "bigint AUTO_INCREMENT",
            'oracle': "NUMBER(19)",
            'postgresql': "bigserial",
            'postgresql_psycopg2': "bigserial",
            'sqlite3': "integer", # Not a bigint!!!
        }

        def db_type(self):
            try:
                for backend, db_type in self.CREATION_DATA.items():
                    try:
                        module = load_backend(backend)
                        if isinstance(connection, getattr(module, 'DatabaseWrapper')):
                            return db_type
                    except (ImportError, exceptions.ImproperlyConfigured):
                        pass
            except (KeyError, AttributeError):
                pass
            raise exceptions.ImproperlyConfigured("BigAutoField does not support the %s database backend" % settings.DATABASE_ENGINE)

        def get_internal_type(self):
            return "BigAutoField"
        
        def to_python(self, value):
            if value is None:
                return value
            try:
                return long(value)
            except (TypeError, ValueError):
                raise exceptions.ValidationError(
                    _("This value must be a long integer."))

    class BigForeignKey(models.ForeignKey):
        
        def db_type(self):
            rel_field = self.rel.get_related_field()
            # next lines are the "bad tooth" in the original code:
            if (isinstance(rel_field, models.AutoField) or
                    (not connection.features.related_fields_match_type and
                    isinstance(rel_field, (PositiveBigIntegerField,
                                           models.PositiveIntegerField,
                                           models.PositiveSmallIntegerField)))):
                # because it continues here in the django code:
                # return IntegerField().db_type()
                # thereby fixing any AutoField as IntegerField
                return BigIntegerField().db_type()
            return rel_field.db_type()

class PositiveBigIntegerField(BigIntegerField):
    # Note: Same internal type as BigIntegerField

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

try:
    from south.modelsinspector import add_introspection_rules

    south_rules = [
      (
        (BigForeignKey,),
        [],
        {
            "to": ["rel.to", {}],
            "to_field": ["rel.field_name", {"default_attr": "rel.to._meta.pk.name"}],
            "related_name": ["rel.related_name", {"default": None}],
            "db_index": ["db_index", {"default": True}],
        },
      ),
    ]
    add_introspection_rules(south_rules, [r"^commons\.models"])
except ImportError:
    pass
