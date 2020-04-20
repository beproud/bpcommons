# vim:fileencoding=utf-8

from six import text_type

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
        if field.remote_field and not check_related:
            continue
        if field.name in exclude:
            continue
        if field.remote_field and check_related_id:
            v1 = getattr(base_obj, field.name + '_id')
            v2 = getattr(new_obj, field.name + '_id')
        else:
            v1 = getattr(base_obj, field.name)
            v2 = getattr(new_obj, field.name)
        if v1 != v2:
            if field.choices or field.remote_field and display:
                if field.remote_field and v1 is None:
                    _v1 = None
                else:
                    _v1 = getattr(base_obj, field.name)
                if field.remote_field and v2 is None:
                    _v2 = None
                else:
                    _v2 = getattr(new_obj, field.name)
                diff_dict[field] = (
                    text_type(_v1 or ''),
                    text_type(_v2 or '')
                )
            else:
                diff_dict[field] = (v1, v2)
    if check_related:
        for field in base_obj._meta.many_to_many:
            if field.name in exclude:
                continue
            # base_objが作成されていない場合
            if base_obj.pk:
                m1 = getattr(base_obj, field.name)
                ids1 = list(m1.values_list('id', flat=True))
            else:
                ids1 = []
            m2 = getattr(new_obj, field.name)
            ids2 = list(m2.values_list('id', flat=True))
            if len(ids1) == len(ids2) == len(set(ids1 + ids2)):
                # 変更なし
                continue
            # add attr
            field.many_to_many = True
            # base_objが作成されていない場合
            if base_obj.pk:
                m1_all = m1.all()
            else:
                m1_all = []
            diff_dict[field] = (
                m1_all,
                m2.all()
            )
    return diff_dict


def copy_obj(from_obj, to_obj, check_primary_key=False, check_related=False, exclude=[], copy_related_id=False, check_many_to_many=False):
    """
    モデルインスタンスのフィールドの内容をコピーする
    """
    for field in from_obj._meta.fields:
        if field.primary_key and not check_primary_key:
            continue
        if field.remote_field and not check_related:
            continue
        if field.name in exclude:
            continue
        if field.remote_field and copy_related_id:
            v = getattr(from_obj, field.name + '_id')
            setattr(to_obj, field.name + '_id', v)
        else:
            v = getattr(from_obj, field.name)
            setattr(to_obj, field.name, v)
    if check_many_to_many:
        # m2mを設定するため保存する
        to_obj.save()
        for field in from_obj._meta.many_to_many:
            if field.name in exclude:
                # 変更なし
                continue
            m1 = getattr(from_obj, field.name)
            m2 = getattr(to_obj, field.name)
            ids1 = list(m1.values_list('id', flat=True))
            ids2 = list(m2.values_list('id', flat=True))
            if len(ids1) == len(ids2) == len(set(ids1 + ids2)):
                continue
            # コピー m1 -> m2
            m2.clear()
            m2_model = m2.model
            for obj in m1.all():
                m2.add(m2_model.objects.get(pk=obj.pk))
