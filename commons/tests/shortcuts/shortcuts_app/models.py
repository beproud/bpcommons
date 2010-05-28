# vim:fileencoding=utf8

from commons.models import BaseModel
from django.db import models

class ShortcutModel(BaseModel):
    name = models.CharField(u"Name", max_length=20)
