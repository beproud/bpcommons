#:coding=utf-8:

from django.test import TestCase as DjangoTestCase


class CacheGetTestCase(DjangoTestCase):

    def test_cache_get(self):
        from beproud.django.commons.utils.cache import cache_get

        test_val = []
        def get_val():
            test_val.append("test")
            return "test-val"
        cached_val = cache_get("test-cache-get", get_val)
        self.assertEqual(cached_val, "test-val")
        self.assertEqual(test_val, ["test"])

        test_val = []
        cached_val = cache_get("test-cache-get", get_val)
        self.assertEqual(cached_val, "test-val")
        self.assertEqual(test_val, [])
