from django.db import models

class BaseManager(models.Manager):
    def be(self):
        return self.filter(del_flg=False)
