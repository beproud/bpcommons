# vim:fileencoding=utf8
from django.db import models

__all__ = (
    'BigIntegerField',
    'PositiveBigIntegerField',
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
