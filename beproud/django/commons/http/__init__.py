# vim:fileencoding=utf-8

import warnings

from django.http import JsonResponse

__all__ = (
    'JSONResponse',
)


class JSONResponse(JsonResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """
    def __init__(self, data={}, status=200, content_type='application/json'):
        warnings.warn('beproud.django.commons.http.JSONResponse was deprecated. Use django.http.JsonResponse instead.', DeprecationWarning)
        super(JSONResponse, self).__init__(data, status=status, content_type=content_type)
