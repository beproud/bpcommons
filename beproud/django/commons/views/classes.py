#:coding=utf-8:
import warnings


__all__ = (
    'Views',
)


class Views(object):
    default_name = ''

    def __init__(self, name=None, app_name=None):
        if name is None:
            self.name = self.default_name
        else:
            self.name = name
        if self.name:
            warnings.warn(
                'beproud.django.commons.views.classes.Views: Attribute'
                ' `default_name` and constructor prametor `name` has been'
                ' Removed. It doesn\'t effect anymore.', DeprecationWarning)

        if app_name is None:
            self.app_name = self.default_name
        else:
            self.app_name = app_name

    def get_urls(self):
        return []

    @property
    def urls(self):
        return self.get_urls(), self.app_name
