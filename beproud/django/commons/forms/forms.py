#:coding=utf-8:

__all__ = ['sort_form_field']


def sort_form_field(form_class, field_names):
    """
    フォームクラスのフィールドをソートする
    field_namesに与えたフィールドを優先する
    """
    def _key(c):
        return -len(field_names) + field_names.index(c) if c in field_names else 1
    form_class.base_fields.keyOrder.sort(key=_key)
