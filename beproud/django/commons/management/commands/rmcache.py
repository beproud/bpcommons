import sys

from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = "delete cache with key name"

    def handle(self, *args, **options):
        if len(args) == 0:
            sys.stdout.write('please input key name.')
            return
        for key in args:
            val = cache.get(key)
            if val is not None:
                cache.delete(key)
                sys.stdout.write('deleting cache: %s, %s' % (key, val))
