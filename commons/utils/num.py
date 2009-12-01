# vim:fileencoding=utf8

def force_int(num, default=None):
    i = default
    try:
        i = int(num)
    except :
        pass
    return i
