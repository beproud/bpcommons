#:coding=utf-8:

from beproud.django.commons.models import DatedModel, BaseModel


class TestDatedModel(DatedModel):
    class Meta:
        app_label = 'base'


class TestBaseModel(BaseModel):
    class Meta:
        app_label = 'base'
