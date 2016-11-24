#:coding=utf-8:

from beproud.django.commons.models import (
    DatedModel as DatedModelBase,
    BaseModel as BaseModelBase
)


class DatedModel(DatedModelBase):
    class Meta:
        app_label = 'base'


class BaseModel(BaseModelBase):
    class Meta:
        app_label = 'base'
