#:coding=utf-8:
import os

from django.db import models
from django.db import connection
from django.test import TestCase as DjangoTestCase
from django.core.exceptions import ValidationError

from beproud.django.commons.models import BigIntegerField
from beproud.django.commons.tests.models.fields.models import (
    TestBigIntModel,
    TestBigToSmallModel,
    ManyToManyTestModel,
    BigIDModel,
)

here = os.path.dirname(__file__)


class BigForeignKeyTest(DjangoTestCase):
    fixtures = [os.path.join(here, 'fixtures', 'initial_data.json')]

    def test_simple(self):
        qs = TestBigIntModel.objects.recently_updated()

        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)

        for obj in qs:
            self.assertTrue(obj.big_id_obj_id)
            self.assertTrue(obj.big_id_obj.id)

    def test_bigtosmall(self):
        qs = TestBigToSmallModel.objects.recently_updated()

        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)

        for obj in qs:
            self.assertTrue(obj.small_id_obj_id)
            self.assertTrue(obj.small_id_obj.id)

    def test_bigforeignkey_db_type(self):
        qs = TestBigIntModel.objects.recently_updated()
        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)
        for obj in qs:
            for f in obj._meta.fields:
                if f.name == "big_id_obj":
                    db_type = f.db_type(connection)
                    bigint_type = BigIntegerField().db_type(connection=connection)
                    self.assertEquals(db_type, bigint_type)  # oracleでは動かない

        qs = TestBigToSmallModel.objects.recently_updated()
        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)
        for obj in qs:
            for f in obj._meta.fields:
                if f.name == "small_id_obj":
                    db_type = f.db_type(connection)
                    int_type = models.IntegerField().db_type(connection=connection)
                    self.assertEquals(db_type, int_type)  # oracleでは動かない

    def test_manytomany_db_type(self):
        for obj in ManyToManyTestModel.objects.all():
            bigids = obj.bigids.all()
            self.assertTrue(len(bigids) > 0)
            for bigid in bigids:
                self.assertTrue(bigid.id)


class BadBigAutoIdTest(DjangoTestCase):
    def test_bad_id(self):
        try:
            BigIDModel._meta.pk.to_python("bad id")
            self.fail("Expected fail")
        except ValidationError:
            pass
