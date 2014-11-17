#:coding=utf-8:

from django.db import models

from beproud.django.commons.models import (
    BaseModel,
    BigAutoField,
    JSONField,
)


class BigIDModel(BaseModel):
    id = BigAutoField(primary_key=True)

    class Meta:
        app_label = 'fields'


class TestBigIntModel(BaseModel):
    big_id_obj = models.ForeignKey(BigIDModel)

    class Meta:
        app_label = 'fields'


class SmallIDModel(BaseModel):
    class Meta:
        app_label = 'fields'


class TestBigToSmallModel(BaseModel):
    small_id_obj = models.ForeignKey(SmallIDModel)

    class Meta:
        app_label = 'fields'


class ManyToManyTestModel(BaseModel):
    bigids = models.ManyToManyField(BigIDModel)

    class Meta:
        app_label = 'fields'


class JSONFieldTestModel(models.Model):
    json = JSONField(u"test", null=True, blank=True)

    class Meta:
        app_label = 'fields'
