#:coding=utf-8:

from django.db import models

from beproud.django.commons.models import (
    BaseModel,
    BigAutoField,
)


class BigIDModel(BaseModel):
    id = BigAutoField(primary_key=True)
    class Meta:
        app_label = 'fields'


class BigIntModel(BaseModel):
    big_id_obj = models.ForeignKey(BigIDModel, on_delete=models.CASCADE)
    class Meta:
        app_label = 'fields'


class SmallIDModel(BaseModel):
    class Meta:
        app_label = 'fields'


class BigToSmallModel(BaseModel):
    small_id_obj = models.ForeignKey(SmallIDModel, on_delete=models.CASCADE)
    class Meta:
        app_label = 'fields'


class ManyToManyModel(BaseModel):
    bigids = models.ManyToManyField(BigIDModel)
    class Meta:
        app_label = 'fields'
