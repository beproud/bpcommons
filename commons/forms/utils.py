# vim:fileencoding=utf-8
def with_empty_tuple(tp, add=('', '--')):
    l = list(tp)
    l.insert(0, add)
    return tuple(l)
