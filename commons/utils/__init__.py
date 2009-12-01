# vim:fileencoding=utf8
from datetime import datetime,date,timedelta
from django.utils.hashcompat import md5_constructor
from django.template.defaultfilters import escapejs
from django.conf import settings
import hashlib

class Bag(object):
    def __init__(self, **kw):
        """Initialise, and set attributes from all keyword arguments."""
        self.__allow_access_to_unprotected_subobjects__=1
        self.__members=[]
        for k in kw.keys():
            setattr(self,k,kw[k])
            self.__remember(k)

    def __remember(self, k):
        """Add k to the list of explicitly set values."""
        if not k in self.__members:
            self.__members.append(k)

    def __getitem__(self, key):
        """Equivalent of dict access by key."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError, key

    def __setitem__(self, key, value):
        setattr(self, key, value)
        self.__remember(key)

    def has_key(self, key):
        return hasattr(self, key)

    def keys(self):
        return self.__members

    def iterkeys(self):
        return self.__members

    def __iter__(self):
        return iter(self.__members)

    def __str__(self):
        """Describe only those attributes explicitly set."""
        s = ""
        for x in self.__members:
            v = getattr(self, x)
            if s: s+=", "
            s += "%s: %s" % (x, `v`)
        return s

def sha_hash(str, sha_method="512"):
    """
    """
    h = getattr(hashlib, "sha%s" % sha_method)()
    h.update((u"itto%sku" % str).encode('utf8')) # これはsoodaと同じである必要がある
    #h.update((u"al3xU%sba3" % str).encode('utf8')) # hash前に適当な文字列を加えている
    return h.hexdigest()

def make_random_key(size=128):
    """
    sizeで指定した長さのランダムなキーを生成
    利用される文字の範囲はa-zA-Z0-9
    """
    from random import sample
    keys = "" 
    src = [x for x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
    while True:
        diff = size - len(keys)
        if diff == 0 : break
        keys += "".join(sample(src,(diff < 20 and diff or 20)))
    return keys

def make_choices_and_dict(tuptup):
    choices = [(x[0],x[2]) for x in tuptup]
    const = dict([ (x[1],x[0]) for x in tuptup ])
    return choices, const

def make_choices_and_value(tuptup):
    values = dict([ (x[0],x[3]) for x in tuptup ])
    keys = dict([ (x[0],x[1]) for x in tuptup ])
    return make_choices_and_dict(tuptup) + (values, keys)

def add_empty_tuple(tp ,add=("","--")):
    l = list(tp)
    l.insert(0,add)
    return tuple(l)
