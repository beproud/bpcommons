#:coding=utf-8:

from django.test import TestCase as DjangoTestCase
from django.core.exceptions import ValidationError

from commons.models import *

class BigIDModel(BaseModel):
    id = BigAutoField(primary_key=True)

class TestBigIntModel(BaseModel):
    big_id_obj = BigForeignKey(BigIDModel)
 
class SmallIDModel(BaseModel):
    pass

class TestBigToSmallModel(BaseModel):
    small_id_obj = BigForeignKey(SmallIDModel)

class BigForeignKeyTest(DjangoTestCase):

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
                    self.assertEquals(f.db_type(), 'bigint') # oracleでは動かない

        qs = TestBigToSmallModel.objects.recently_updated()
        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)
        for obj in qs:
            for f in obj._meta.fields:
                if f.name == "small_id_obj":
                    self.assertEquals(f.db_type(), 'bigint') # oracleでは動かない

class BadBigAutoIdTest(DjangoTestCase):
    def test_bad_id(self):
        try:
            bad_id = BigIDModel._meta.pk.to_python("bad id")
            self.fail("Expected fail")
        except ValidationError:
            pass
