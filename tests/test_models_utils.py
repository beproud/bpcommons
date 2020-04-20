# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
import factory

from models.base.models import BaseModel


__all__ = (
    'TestCompareModel',
    'TestCopyModel',
)


class BaseModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseModel


@pytest.mark.django_db
class TestCompareModel(object):

    @pytest.fixture
    def target(self):
        from beproud.django.commons.models.utils import compare_obj
        return compare_obj

    def test_simple(self, target):
        base_obj = BaseModelFactory.create(del_flg=False)
        new_obj = BaseModelFactory.create(del_flg=True)
        result = target(base_obj, new_obj)

        del_flg_field = BaseModel._meta.get_field("del_flg")
        assert result[del_flg_field] == (False, True)


@pytest.mark.django_db
class TestCopyModel(object):

    @pytest.fixture
    def target(self):
        from beproud.django.commons.models.utils import copy_obj
        return copy_obj

    def test_simple(self, target):
        from_obj = BaseModelFactory.create(utime=datetime(2020, 4, 20))
        to_obj = BaseModel()
        target(from_obj, to_obj)

        assert from_obj.id != to_obj.id
        assert from_obj.ctime == to_obj.ctime
        assert from_obj.utime == to_obj.utime
        assert from_obj.del_flg == to_obj.del_flg
