#:coding=utf-8:

import base64
import warnings

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    import json
except ImportError:
    import simplejson as json

from django import VERSION as DJANGO_VERSION
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
try:
   from django.db import load_backend
except ImportError:
   from django.db.utils import load_backend
from django.db.models import BigIntegerField

from django.db import models

from beproud.django.commons.forms import JSONField as JSONFormField
from beproud.django.commons.forms.widgets import JSONWidget
from beproud.django.commons.utils.javascript import DjangoJSONEncoder

__all__ = (
    'BigIntegerField',
    'PositiveBigIntegerField',
    'BigAutoField',
    'PickledObjectField',
    'JSONField',
)


class BigAutoField(models.AutoField):
    description = _("Big (8 byte) integer")

    CREATION_DATA = {
        'django.db.backends.mysql': "bigint AUTO_INCREMENT",
        'django.db.backends.oracle': "NUMBER(19)",
        'django.db.backends.postgresql': "bigserial",
        'django.db.backends.postgresql_psycopg2': "bigserial",
        'django.db.backends.sqlite3': "integer",  # NOTE: Not a bigint!!!
    }

    def db_type(self, connection):
        try:
            for backend, db_type in self.CREATION_DATA.items():
                try:
                    module = load_backend(backend)
                    DatabaseWrapper = getattr(module, 'DatabaseWrapper')
                    if isinstance(connection, DatabaseWrapper):
                        return db_type
                    elif DJANGO_VERSION >= (1, 7):
                        from django.db import DefaultConnectionProxy, connections
                        from django.db.utils import DEFAULT_DB_ALIAS
                        if (isinstance(connection, DefaultConnectionProxy) and

                                isinstance(connections[DEFAULT_DB_ALIAS], DatabaseWrapper)):
                            return db_type
                except (ImportError, exceptions.ImproperlyConfigured):
                    pass
        except (KeyError, AttributeError):
            pass
        raise exceptions.ImproperlyConfigured('BigAutoField does not support the "%s" database '
                                              'backend' % connection.settings_dict["ENGINE"])

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


def fk_db_type(self, connection):
    # The database column type of a ForeignKey is the column type
    # of the field to which it points. An exception is if the ForeignKey
    # points to an AutoField/PositiveIntegerField/PositiveSmallIntegerField,
    # in which case the column type is simply that of an IntegerField.
    # If the database needs similar types for key fields however, the only
    # thing we can do is making AutoField an IntegerField.
    rel_field = self.rel.get_related_field()

    if (isinstance(rel_field, BigAutoField) or
            (not connection.features.related_fields_match_type and
             isinstance(rel_field, PositiveBigIntegerField))):
        return BigIntegerField().db_type(connection=connection)

    if (isinstance(rel_field, models.AutoField) or
            (not connection.features.related_fields_match_type and
             isinstance(rel_field, (models.PositiveIntegerField,
                                    models.PositiveSmallIntegerField)))):
        return models.IntegerField().db_type(connection=connection)
    return rel_field.db_type(connection=connection)

# ForeignKey monkey-patch to support BigAutoId
models.ForeignKey.db_type = fk_db_type


class PositiveBigIntegerField(BigIntegerField):
    # Note: Same internal type as BigIntegerField

    def formfield(self, **kwargs):
        defaults = {'min_value': 0}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)


class PickledObjectField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        warnings.warn('PickledObjectField is deprecated. Use django-picklefield instead.')
        super(PickledObjectField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, basestring):
            return value
        return pickle.loads(base64.b64decode(value))

    def get_db_prep_save(self, value, connection=None):
        if value is None:
            return
        return base64.b64encode(pickle.dumps(value))


class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        warnings.warn('JSONField is deprecated. Use django-jsonfield instead.')
        super(JSONField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': JSONWidget, 'form_class': JSONFormField}
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

    def to_python(self, value):
        # If value is a bastring but empty then pass
        if isinstance(value, basestring):
            if value == '':
                return None
            else:
                value = json.loads(value)
        return value

    def get_db_prep_value(self, value, connection=None, prepared=None):
        if value is None:
            return
        return json.dumps(value, cls=DjangoJSONEncoder)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([

        ((BigAutoField,), [], {},),

    ], [r"^beproud\.django\.commons\.models"])
except ImportError:
    pass
