#:coding=utf-8:
from django import forms


def autostrip(cls):
    """
    strip text fields before validation

    example:
    class PersonForm(forms.Form):
        name = forms.CharField(min_length=2, max_length=10)
        email = forms.EmailField()

    PersonForm = autostrip(PersonForm)
    
    #or you can use @autostrip in python >= 2.6

    Author: nail.xx

    Taken from django-annoying
    """
    fields = [(key, value) for key, value in cls.base_fields.items() if isinstance(value, forms.CharField)]
    for field_name, field_object in fields:
        def get_clean_func(original_clean):
            return lambda value: original_clean(value and value.strip())
        clean_func = get_clean_func(getattr(field_object, 'clean'))
        setattr(field_object, 'clean', clean_func)
    return cls
