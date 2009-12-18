# vim:fileencoding=utf-8

__all__ = (
    'compare_obj',
    'copy_obj',
)

def compare_obj(base_obj, new_obj, check_primary_key=False, check_related=False, exclude=[]):
    """
    モデルインスタンスの比較を行う
    差分を辞書で返す
    """
    diff_dict = {}
    for field in base_obj._meta.fields:
        if field.primary_key and not check_primary_key:
            continue
        if field.rel and not check_related:
            continue
        if field.name in exclude:
            continue
        v1 = getattr(base_obj, field.name)
        v2 = getattr(new_obj, field.name)
        if v1 != v2:
            diff_dict[field] = (v1, v2)
    return diff_dict

def copy_obj(from_obj, to_obj, check_primary_key=False, check_related=False, exclude=[]):
    """
    モデルインスタンスのフィールドの内容をコピーする
    """
    for field in from_obj._meta.fields:
        if field.primary_key and not check_primary_key:
            continue
        if field.rel and not check_related:
            continue
        if field.name in exclude:
            continue
        v = getattr(from_obj, field.name)
        setattr(to_obj, field.name, v)
