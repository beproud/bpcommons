#:coding=utf-8:

from django.contrib import admin

class DatedModelAdmin(admin.ModelAdmin):
    u"""
    DatedModel のサブクラスの管理画面用のベースクラス

    system_fields という設定を追加する。
    system_fields は管理用のフィールドをタップルで定義します。
    定義するフィールドは「システム管理」というフィールドセットで
    分けて、デフォールトで隠します。

    declared_fieldsets を定義すれば、system_fields は無視されます

    system_fields のデフォールトは::
    
        system_fields = ('ctime', 'utime')

    デフォールト設定を外したい場合は None を設定すれば、
    外せます::

        system_fields = None

    使い方::

        class MyModelAdmin(DatedModelAdmin):
            list_display = ('myfield', 'del_flg', 'utime', 'ctime')
            system_fields = ('my_system_field',) + DatedModelAdmin.system_fields
            #...
    """
    date_hierarchy = 'ctime'
    list_display = ('__str__', 'utime', 'ctime')
    readonly_fields = ('ctime', 'utime')

    system_fields = ('ctime', 'utime')

    def get_fieldsets(self, request, obj=None):
        u"""
        デフォールトで
        """
        if self.declared_fieldsets:
            return self.declared_fieldsets
        if self.system_fields is None:
            return super(DatedModelAdmin, self).get_fieldsets(request, obj)

        form = self.get_form(request, obj)
        fields = list(form.base_fields.keys()) + list(self.get_readonly_fields(request, obj))
        normal_fields = [f for f in fields if f not in self.system_fields]

        return (
            (None, {'fields': normal_fields}),
            (u"システム管理", {
                'classes': ('collapse',),
                'fields': self.system_fields, 
            }),
        )

class BaseModelAdmin(DatedModelAdmin):
    u"""
    BaseModel のサブクラスの管理画面用のベースクラス

    使い方:: 

        class MyModelAdmin(BaseModelAdmin):
            list_display = ('myfield', 'del_flg', 'utime', 'ctime')
    """
    list_display = ('__str__', 'del_flg', 'utime', 'ctime')
    system_fields = ('del_flg', 'ctime', 'utime')
