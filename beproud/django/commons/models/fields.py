#:coding=utf-8:

from django import VERSION as DJANGO_VERSION
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
try:
   from django.db import load_backend
except ImportError:
   from django.db.utils import load_backend
from django.db.models import BigIntegerField

from django.db import models


__all__ = (
    'PositiveBigIntegerField',
    'BigAutoField',
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
                    else:  # DJANGO_VERSION >= (1, 7):
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
        return int(value)

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(self.error_messages['invalid'])


def fk_db_type(self, connection):
    # The database column type of a ForeignKey is the column type
    # of the field to which it points. An exception is if the ForeignKey
    # points to an AutoField/PositiveIntegerField/PositiveSmallIntegerField,
    # in which case the column type is simply that of an IntegerField.
    # If the database needs similar types for key fields however, the only
    # thing we can do is making AutoField an IntegerField.
    if DJANGO_VERSION >= (1, 9):
        rel_field = self.remote_field.get_related_field()
    else:  # for django-1.8
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


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([

        ((BigAutoField,), [], {},),

    ], [r"^beproud\.django\.commons\.models"])
except ImportError:
    pass
