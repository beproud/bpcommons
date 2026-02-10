.. release procedure

Procedure:

1. check CI status testing result: https://github.com/beproud/bpcommons/actions
2. update release version/date in ``ChangeLog.rst``
3. run ``python -m build .``
4. check ``twine check --strict dist/*``
5. upload testpypi ``twine upload --repository testpypi dist/*``
6. check description, and uploaded build package.
7. upload ``twine upload dist/*``
8. tagging version e.g. ``git tag v0.40``.
9. check PyPI page: https://pypi.org/p/beproud.django.commons/
10. bump versions and commit/push them onto GitHub

   * ``ChangeLog.rst``  next version
   * ``beproud/django/commons/__init__.py`` next version
