# vim:fileencoding=utf-8
from django.core.cache import cache

__all__ = (
    'cache_get',
)

def cache_get(key, func, timeout=None, too_empty=False):
    """
    キャッシュにあれば使う、なければfuncを実行してキャッシュする
    too_empty=Trueにすると空の場合もキャッシュする
    """
    val = cache.get(key)
    if (not val) if too_empty else (val is None):
        val = func()
        cache.set(key, val, timeout)
    return val
