.. release procedure

Procedure:

1. check CI status testing result: https://github.com/beproud/bpcommons/actions
2. update release version/date in ``ChangeLog.rst``
3. tagging version e.g. ``git tag 0.40``.
5. run ``python setup.py release sdist bdist_wheel``
6. upload ``twine upload dist/*``
7. check PyPI page: https://pypi.org/p/beproud.django.commons/
8. bump versions and commit/push them onto GitHub
    * ``ChangeLog.rst``  next version
    * ``bpcommons/beproud/django/commons/__init__.py`` next version
