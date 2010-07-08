#:coding=utf-8:

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

    def test_remove(self):
        obj = TestBaseModel.objects.get(pk=1)
        self.assertTrue(not obj.del_flg)

        obj.remove()
        self.assertTrue(obj.del_flg)

        obj_updated = TestBaseModel.objects.get(pk=1)
        self.assertTrue(obj_updated.del_flg)

    def test_unremove(self):
        obj = TestBaseModel.objects.get(pk=3)
        self.assertTrue(obj.del_flg)

        obj.unremove()
        self.assertTrue(not obj.del_flg)

        obj_updated = TestBaseModel.objects.get(pk=3)
        self.assertTrue(not obj_updated.del_flg)
