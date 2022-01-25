.. release procedure

Procedure:

1. check CI status testing result: https://github.com/beproud/bpcommons/actions
2. update release version/date in ``ChangeLog.rst``
3. run ``python setup.py release sdist bdist_wheel``
4. check ``twine check dist/*``
5. upload ``twine upload dist/*``
6. tagging version e.g. ``git tag v0.40``.
7. check PyPI page: https://pypi.org/p/beproud.django.commons/
8. bump versions and commit/push them onto GitHub

   * ``ChangeLog.rst``  next version
   * ``bpcommons/beproud/django/commons/__init__.py`` next version
