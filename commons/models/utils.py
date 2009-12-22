# vim:fileencoding=utf-8

__all__ = (
    'compare_obj',
    'copy_obj',
)

def compare_obj(base_obj, new_obj, check_primary_key=False, check_related=False, exclude=[], check_related_id=False, display=False):
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
        if field.rel and check_related_id:
            v1 = getattr(base_obj, field.name + '_id')
            v2 = getattr(new_obj, field.name + '_id')
        else:
            v1 = getattr(base_obj, field.name)
            v2 = getattr(new_obj, field.name)
        if v1 != v2:
            if field.choices and display:
                diff_dict[field] = (
                    getattr(base_obj, 'get_%s_display' % field.name)(),
                    getattr(new_obj, 'get_%s_display' % field.name)()
                )
            else:
                diff_dict[field] = (v1, v2)
    return diff_dict

def copy_obj(from_obj, to_obj, check_primary_key=False, check_related=False, exclude=[], copy_related_id=False):
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
        if field.rel and copy_related_id:
            v = getattr(from_obj, field.name + '_id')
            setattr(to_obj, field.name + '_id', v)
        else:
            v = getattr(from_obj, field.name)
            setattr(to_obj, field.name, v)
