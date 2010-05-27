# vim:fileencoding=utf8

from django.test import TestCase as DjangoTestCase

from commons.models import DatedModel, BaseModel

class TestDatedModel(DatedModel):
    pass

class TestBaseModel(BaseModel):
    pass

class DatedModelTest(DjangoTestCase):

    def test_simple(self):
        qs = TestDatedModel.objects.recently_updated()

        # クエリがデータを返すかどうかをチェック
        self.assertTrue(qs)

        previous = None
        for obj in qs:
            if previous:
                self.assertTrue(obj.utime <= previous.utime)
            previous = obj

class BaseModelTest(DjangoTestCase):

    def test_existing(self):
        qs = TestBaseModel.existing.recently_updated()
        
        previous = None
        for obj in qs:
            if previous:
                self.assertTrue(obj.utime <= previous.utime)
            self.assertTrue(not obj.del_flg)
            previous = obj

