# vim:fileencoding=utf-8
def with_empty_tuple(tp, add=('', '--')):
    l = list(tp)
    l.insert(0, add)
    return tuple(l)

def make_choices_and_dict(tuptup):
    choices = [(x[0],x[2]) for x in tuptup]
    const = dict([ (x[1],x[0]) for x in tuptup ])
    return choices, const

def make_choices_and_value(tuptup):
    values = dict([ (x[0],x[3]) for x in tuptup ])
    keys = dict([ (x[0],x[1]) for x in tuptup ])
    return make_choices_and_dict(tuptup) + (values, keys)
