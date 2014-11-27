#:coding=utf-8:

# NOTE: Django 1.6 以上の場合はテストランナーは test*.py
# というパターンにマッチするファイルしか認識しないので、
# このファイル (__init__.py) に入っているテストは認識しない。
# このファイルは主に Django 1.5以下のテストランナーのために
# テストをインポートしています。

from beproud.django.commons.tests.test_javascript import *  # NOQA
from beproud.django.commons.tests.test_template import *  # NOQA
from beproud.django.commons.tests.test_cache import *  # NOQA
from beproud.django.commons.tests.test_views import *  # NOQA
from beproud.django.commons.tests.test_templatetags import *  # NOQA
from beproud.django.commons.tests.test_http import *  # NOQA
from beproud.django.commons.tests.test_shortcuts import *  # NOQA

from beproud.django.commons.tests.models.base.tests import *  # NOQA
from beproud.django.commons.tests.models.fields.tests import *  # NOQA

from beproud.django.commons.tests.forms.test_field import *  # NOQA
