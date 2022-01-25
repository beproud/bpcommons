.. release procedure

Procedure:

1. check CI status testing result: https://github.com/beproud/bpcommons/actions
2. update release version/date in ``ChangeLog.rst``
3. tagging version e.g. ``git tag v0.40``.
4. run ``python setup.py release sdist bdist_wheel``
5. upload ``twine upload dist/*``
6. check PyPI page: https://pypi.org/p/beproud.django.commons/
7. bump versions and commit/push them onto GitHub

   * ``ChangeLog.rst``  next version
   * ``bpcommons/beproud/django/commons/__init__.py`` next version
