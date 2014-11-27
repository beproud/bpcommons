#:coding=utf-8:

from django.db import models

from beproud.django.commons.models import (
    BaseModel,
    BigAutoField,
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
