=========
ChangeLog
=========

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

