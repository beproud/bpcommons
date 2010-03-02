# vim:fileencoding=utf8
from django.db import models
from datetime import datetime

__all__ = (
    'DatedModelManager',
    'DatedModel',
    'BaseManager',
    'BaseModel',
)

class DatedModelManager(models.Manager):
    def recently_updated(self):
        return self.order_by('-utime')

class DatedModel(models.Model):
    """
    日付が付けたモデル
    """
    ctime = models.DateTimeField(u'作成日時', default=datetime.now, db_index=True)
    utime = models.DateTimeField(u'更新日時', auto_now=True, db_index=True) 

    objects = DatedModelManager()

    class Meta:
        abstract = True
        ordering = ['-ctime']

class BaseManager(DatedModelManager):
    def get_query_set(self):
        return super(BaseManager, self).get_query_set().filter(pub_flg=True)

    def recently_updated(self):
        return self.order_by('-utime')

class BaseModel(DatedModel):
    """
    BaseModelの実装
    
    使い方:
    from django.db import models
    from commons.models import BaseModel

    class MyModel(BaseModel):
        myfield = models.BooleanField()

    MyModel.published.filter(myfield=True)
    """
    pub_flg = models.BooleanField(u'公開フラグ', default=True, db_index=True)

    objects = DatedModelManager()
    published = BaseManager()

    def remove(self):
        self.pub_flg = False
        self.save()

    def publish(self):
        self.pub_flg = True 
        self.save()

    class Meta:
        abstract = True
        ordering = ['-ctime']
