#:coding=utf-8:
from datetime import datetime

import pytest
import factory
from django.db import connection
from django.core.exceptions import ValidationError
from django.db.models import IntegerField, BigIntegerField

from models.fields.models import (
    BigIntModel,
    BigToSmallModel,
    ManyToManyModel,
    BigIDModel,
    SmallIDModel,
)


class BigIdModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BigIDModel

    id = factory.Sequence(lambda n: n * 10000000 + 1)


class SmallIDModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmallIDModel


class BigIntModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BigIntModel

    big_id_obj = factory.SubFactory(BigIdModelFactory)


class BigToSmallModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BigToSmallModel

    small_id_obj = factory.SubFactory(SmallIDModelFactory)


class ManyToManyModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ManyToManyModel

    @factory.post_generation
    def bigids(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for bigid in extracted:
                self.bigids.add(bigid)


@pytest.mark.django_db
class TestBigForeignKey(object):

    @pytest.fixture
    def make_bigid(self):
        return BigIdModelFactory.create

    @pytest.fixture
    def make_bigint(self):
        return BigIntModelFactory.create

    @pytest.fixture
    def make_bigtosmall(self):
        return BigToSmallModelFactory.create

    @pytest.fixture
    def make_manytomany(self):
        return ManyToManyModelFactory.create

    def test_simple(self, make_bigint):
        make_bigint()
        make_bigint()

        qs = BigIntModel.objects.recently_updated()

        # クエリがデータを返すかどうかをチェック
        assert qs

        for obj in qs:
            assert obj.big_id_obj_id

    def test_bigtosmall(self, make_bigtosmall):
        make_bigtosmall()
        make_bigtosmall()

        qs = BigToSmallModel.objects.recently_updated()

        # クエリがデータを返すかどうかをチェック
        assert qs

        for obj in qs:
            assert obj.small_id_obj_id

    def test_bigforeignkey_db_type(self, make_bigint, make_bigtosmall):
        make_bigint()
        make_bigint()
        make_bigtosmall()
        make_bigtosmall()

        qs = BigIntModel.objects.recently_updated()
        # クエリがデータを返すかどうかをチェック
        assert qs
        for obj in qs:
            for f in obj._meta.fields:
                if f.name == "big_id_obj":
                    db_type = f.db_type(connection)
                    bigint_type = BigIntegerField().db_type(connection=connection)
                    assert db_type == bigint_type  # oracleでは動かない

        qs = BigToSmallModel.objects.recently_updated()
        # クエリがデータを返すかどうかをチェック
        assert qs
        for obj in qs:
            for f in obj._meta.fields:
                if f.name == "small_id_obj":
                    db_type = f.db_type(connection)
                    int_type = IntegerField().db_type(connection=connection)
                    assert db_type == int_type  # oracleでは動かない

    def test_manytomany_db_type(self, make_manytomany, make_bigid):
        b1 = make_bigid()
        b2 = make_bigid()
        b3 = make_bigid()
        make_manytomany(bigids=(b1, b2))
        make_manytomany(bigids=[b1])
        make_manytomany(bigids=[b1, b2, b3])

        for obj in ManyToManyModel.objects.all():
            bigids = obj.bigids.all()
            assert len(bigids) > 0
            for bigid in bigids:
                assert bigid.id


@pytest.mark.django_db
class TestBadBigAutoId(object):
    def test_bad_id(self):
        with pytest.raises(ValidationError):
            BigIDModel._meta.pk.to_python("bad id")

