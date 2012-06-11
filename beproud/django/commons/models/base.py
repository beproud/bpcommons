#:coding=utf-8:

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
    def be(self):
        """
        削除されてないBaseModelオブジェクトを取得
        """
        return self.filter(del_flg=False)

class BaseModel(DatedModel):
    """
    BaseModelの実装
    
    使い方:
    from django.db import models
    from commons.models import BaseModel

    class MyModel(BaseModel):
        myfield = models.BooleanField()

    MyModel.existing.filter(myfield=True)
    """
    del_flg = models.BooleanField(u'削除フラグ', default=False)

    objects = BaseManager()

    def remove(self):
        self.del_flg = True
        self.save()

    def unremove(self):
        self.del_flg = False 
        self.save()

    class Meta:
        abstract = True
        ordering = ['-ctime']
