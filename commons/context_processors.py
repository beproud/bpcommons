# vim:fileencoding=utf-8
from django.conf import settings

def debug(request):
    """
    Returns context variables helpful for debugging.
    """
    context_extras = {}
    if settings.DEBUG and getattr(settings, 'TEMPLATE_DEBUG', False):
        context_extras['debug'] = True
        from django.db import connection
        context_extras['sql_queries'] = connection.queries
    return context_extras
