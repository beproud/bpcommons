#:coding=utf-8:


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
        if app_name is None:
            self.app_name = self.default_name
        else:
            self.app_name = app_name

    def get_urls(self):
        return []

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name
