#:coding=utf-8:

from django.test import TestCase as DjangoTestCase
from django.core.exceptions import ValidationError
from django.db import connection
from django.db import models

from beproud.django.commons.models import (
    BaseModel,
    BigAutoField,
    BigIntegerField,
    JSONField,
)

class BigIDModel(BaseModel):
    id = BigAutoField(primary_key=True)

class TestBigIntModel(BaseModel):
    big_id_obj = models.ForeignKey(BigIDModel)
 
class SmallIDModel(BaseModel):
    pass

class TestBigToSmallModel(BaseModel):
    small_id_obj = models.ForeignKey(SmallIDModel)

class ManyToManyTestModel(BaseModel):
    bigids = models.ManyToManyField(BigIDModel)

class JSONFieldTestModel(models.Model):
    json = JSONField(u"test", null=True, blank=True)

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
                    db_type = f.db_type(connection)
                    bigint_type = BigIntegerField().db_type(connection=connection)
                    self.assertEquals(db_type, bigint_type) # oracleでは動かない

        qs = TestBigToSmallModel.objects.recently_updated()
        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)
        for obj in qs:
            for f in obj._meta.fields:
                if f.name == "small_id_obj":
                    db_type = f.db_type(connection)
                    int_type = models.IntegerField().db_type(connection=connection)
                    self.assertEquals(db_type, int_type) # oracleでは動かない

    def test_manytomany_db_type(self):
        for obj in ManyToManyTestModel.objects.all():
            bigids = obj.bigids.all()
            self.assertTrue(len(bigids) > 0)
            for bigid in bigids:
                self.assertTrue(bigid.id)

class BadBigAutoIdTest(DjangoTestCase):
    def test_bad_id(self):
        try:
            bad_id = BigIDModel._meta.pk.to_python("bad id")
            self.fail("Expected fail")
        except ValidationError:
            pass

class JSONFieldTest(DjangoTestCase):
    def test_json_field(self):
        obj = JSONFieldTestModel(json='''{
            "spam": "eggs"
        }''')
        self.assertEquals(obj.json, {'spam':'eggs'})

    def test_json_field_empty(self):
        obj = JSONFieldTestModel(json='')
        self.assertEquals(obj.json, None)

    def test_json_field_save(self):
        obj = JSONFieldTestModel.objects.create(
            id=10, 
            json='''{
                "spam": "eggs"
            }''',
        )
        obj2 = JSONFieldTestModel.objects.get(id=10)
        self.assertEquals(obj2.json, {'spam':'eggs'})

    def test_json_field_save_empty(self):
        obj = JSONFieldTestModel.objects.create(id=10, json='')
        obj2 = JSONFieldTestModel.objects.get(id=10)
        self.assertEquals(obj2.json, None)

    def test_db_prep_value(self):
        field = JSONField(u"test")
        field.set_attributes_from_name("json")
        self.assertEquals(None, field.get_db_prep_value(None))
        self.assertEquals('{"spam": "eggs"}', field.get_db_prep_value({"spam": "eggs"}))

    def test_value_to_string(self):
        field = JSONField(u"test")
        field.set_attributes_from_name("json")
        obj = JSONFieldTestModel(json='''{
            "spam": "eggs"
        }''')
        self.assertEquals('{"spam": "eggs"}', field.value_to_string(obj))

    def test_formfield(self):
        from beproud.django.commons.forms import JSONField as JSONFormField
        from beproud.django.commons.forms.widgets import JSONWidget
        field = JSONField(u"test")
        field.set_attributes_from_name("json")
        formfield = field.formfield()
        self.assertEquals(type(formfield), JSONFormField)
        self.assertEquals(type(formfield.widget), JSONWidget)

