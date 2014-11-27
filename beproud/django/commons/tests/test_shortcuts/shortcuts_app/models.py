#:coding=utf-8:

from django.db import models

from beproud.django.commons.models import BaseModel


class ShortcutModel(BaseModel):
    name = models.CharField(u"Name", max_length=20)
