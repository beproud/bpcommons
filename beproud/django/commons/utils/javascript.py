# vim:fileencoding=utf-8

import warnings
from django.core.serializers.json import DjangoJSONEncoder  # NOQA

warnings.warn('beproud.django.commons.utils.javascript.DjangoJSONEncoder was deprecated. Use django.core.serializers.json.DjangoJSONEncoder instead.', DeprecationWarning)
