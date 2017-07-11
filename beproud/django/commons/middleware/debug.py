#:coding=utf-8:

from __future__ import print_function
from django.conf import settings

class DebugMiddleware(object):
    def process_response(self, request, response):
        if settings.DEBUG: 
            from django.db import connection
            for query in connection.queries:
                print(query)
        return response
