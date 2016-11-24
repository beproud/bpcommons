#:coding=utf-8:
from datetime import datetime

import pytest
import factory

from models.base.models import DatedModel, BaseModel


class DatedModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatedModel


class BaseModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BaseModel


@pytest.mark.django_db
class TestDatedModel(object):

    @pytest.fixture
    def create_target(self):
        return DatedModelFactory.create

    def test_simple(self, create_target):
        create_target(utime=datetime(2016, 10, 1))
        create_target(utime=datetime(2016, 10, 3))
        create_target(utime=datetime(2016, 10, 2))

        qs = DatedModel.objects.recently_updated()

        # クエリがデータを返すかどうかをチェック
        assert qs

        previous = None
        for obj in qs:
            if previous:
                assert obj.utime <= previous.utime
            previous = obj


@pytest.mark.django_db
class TestBaseModel(object):

    @pytest.fixture
    def create_target(self):
        return BaseModelFactory.create

    def test_be(self, create_target):
        create_target()
        create_target()
        create_target(del_flg=True)

        qs = BaseModel.objects.be()

        for obj in qs:
            assert not obj.del_flg

    def test_remove(self, create_target):
        obj = create_target()
        assert not obj.del_flg

        obj.remove()
        assert obj.del_flg

        obj_updated = BaseModel.objects.get(pk=1)
        assert obj_updated.del_flg

    def test_unremove(self, create_target):
        obj = create_target(del_flg=True)
        assert obj.del_flg

        obj.unremove()
        assert not obj.del_flg

        obj_updated = BaseModel.objects.get(pk=obj.pk)
        assert not obj_updated.del_flg
