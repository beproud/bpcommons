# vim:fileencoding=utf8
from django.db import models
from datetime import datetime

__all__ = (
    'BaseManager',
    'BaseModel',
)

class BaseManager(models.Manager):
    def get_query_set(self):
        return super(BaseManager, self).get_query_set().filter(del_flg=True)

    def recently_updated(self):
        return self.order_by('-utime')

class BaseModel(models.Model):
    """
    BaseModelの実装
    
    使い方:
    from django.db import models
    from commons.models import BaseModel

    class MyModel(BaseModel):
        myfield = models.BooleanField()

    MyModel.published.filter(myfield=True)
    """
    del_flg = models.BooleanField(u'公開フラグ', default=True, db_index=True)
    ctime = models.DateTimeField(u'作成日時', default=datetime.now, db_index=True)
    utime = models.DateTimeField(u'更新日時', auto_now=True, db_index=True) 

    objects = models.Manager()
    published = BaseManager()

    def remove():
        self.del_flg = False
        self.save()

    class Meta:
        abstract = True
        ordering = ['-ctime']
