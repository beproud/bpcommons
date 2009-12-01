# vim:fileencoding=utf-8
from django.core.cache import cache

def cache_get(key, func, timeout=None):
    """
    キャッシュにあれば使う、なければfuncを実行してキャッシュする
    """
    val = cache.get(key)
    if val is None:
        val = func()
        cache.set(key, val, timeout)
    return val

def has_id_previous_list(list_key,id,list_num=100):
    """
     指定されたIDが指定されたkeyのリストオブジェクトに含まれるかをチェック、
    過去list_num件をさかのぼって存在した場合はTrueを返します
    質問詳細ページのユーザユニークチェックなどに利用
    
    """
    if id == None:
        return False

    list = cache.get(list_key) or []
    if id in list:
        return True
    if len(list) > list_num : list.pop(0)
    list.append(id)
    cache.set(list_key, list)
    return False
