# vim:fileencoding=utf-8

from django.utils.datastructures import SortedDict

__all__ = (
    'Choices',
    'with_empty_tuple',
    'make_choices_and_dict',
    'make_choices_and_value',
)

class Choices(object):
    """
    Easy declarative "choices" tool::
    
        >>> STATUSES = Choices(
        ...     (1, 'live', 'Live'),
        ...     (2, 'draft', 'Draft'),
        ...     (3, 'hidden', 'Not Live'),
        ... )
        
        # Acts like a choices list:
        >>> list(STATUSES)
        [(1, 'Live'), (2, 'Draft')]
        
        # Easily convert from code to verbose:
        >>> STATUSES.verbose(1)
        'Live'

        >>> STATUS.prop(1)
        'live'
        
        # ... and vice versa:
        >>> STATUSES.code("draft")
        2

        status = models.SmallIntegerField(choices=STATUSES,
        ...                                       default=STATUSES["live"])
        
    """
    def __init__(self, *args, **kwargs):
        self.code_map = SortedDict()
        self.prop_map = SortedDict() 
        self.reverse_map = {}
        for code, prop, verbose in args:
            self.code_map[code] = verbose
            self.prop_map[code] = prop
            self.reverse_map[prop] = code
            
    def __iter__(self):
        return self.code_map.iteritems()
                
    def __len__(self):
        return len(self.code_map)

    def __getitem__(self, prop):
        return self.code(prop)

    def __contains__(self, prop):
        return prop in self.reverse_map 

    def code(self, prop):
        """
        Return the code version of the verbose name.
        """
        return self.reverse_map[prop]

    def prop(self, code):
        return self.prop_map[code]
        
    def verbose(self, code):
        """
        Return the verbose name given the code.
        """
        return self.code_map[code]
    
    def __repr__(self):
        return repr(tuple(self.code_map.items()))

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
