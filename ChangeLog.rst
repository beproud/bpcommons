=========
ChangeLog
=========

Release 0.42 (2023-01-24)
==========================

- Support Django-4.1
- Support Python-3.8, 3.9, 3.10, 3.11
- Drop Django-2.2
- Drop Python-3.6, 3.7


Release 0.41 (2022-01-25)
==========================

- Support Django-3.2
- Support Python-3.7, 3.8, 3.9, 3.10
- Drop Django-1.11


Release 0.40 (2020-04-28)
==========================

- Fix: Field.rel and Field.remote_field.to are removed in Django 2.0


Release 0.39 (2019-09-17)
==========================
Supports:

- Python-3.6, 3.7 (+ 3.7 / - 2.7)
- Django-1.11, 2.2 (+ 2.2 / - 1.8, 1.10 that doesn't support py36)
- Drop dependency: zenhan


Release 0.38 (2017-07-11)
=========================
- Support Python-3.6
- Support Django-1.11
- Drop Django-1.9
- Remove dependency to bputils


Release 0.37 (2016-11-25)
=========================

- Support Django-1.10
- Drop Python-2.6
- Drop Django-1.7 or earlier.
- Deprecate some classes:

  - beproud.django.commons.http.JsonResponse
  - beproud.django.commons.utils.javascript.DjangoJSONEncoder

- Drop some classes:

  - beproud.django.commons.models.fields.JSONField
  - beproud.django.commons.models.fields.PickledObjectField
  - beproud.django.commons.forms.JSONField
  - beproud.django.commons.forms.widgets.JSONWidget
  - beproud.django.commons.forms.widgets.AdminJSONWidget

- Drop ``switch`` templatetag.

- Remove 'BigIntegerField' from __all__ of beproud.django.commons.models.fields.
  Please use django.db.models.BigIntegerField instead.

Please use https://pypi.python.org/pypi/jsonfield instead of our JSONField.

Release 0.36 (2016-03-23)
=========================

- some fixes and improvements

Release 0.35 (2016-01-15)
=========================

- Support Django-1.9
- some fixes and improvements

