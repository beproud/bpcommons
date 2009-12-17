# vim:fileencoding=utf8
from django.db import models

__all__ = (
    'BaseManager',
    'BaseModel',
)

class BaseManager(models.Manager):
    def viewable(self):
        return self.filter(published=True)

    def recently_updated(self):
        return self.order_by('-utime')

class BaseModel(models.Model):
    published = models.BooleanField(u'公開フラグ', default=True, db_index=True)
    ctime = models.DateTimeField(u'作成日時', default=datetime.now, db_index=True)
    utime = models.DateTimeField(u'更新日時', auto_now=True, db_index=True) 

    objects = BaseManager()

    def remove():
        self.published = False
        self.save()

    class Meta:
        abstract = True
        ordering = ['-ctime']
