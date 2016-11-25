#:coding=utf-8:

from django.conf.urls import url
from django.http import HttpResponse

from beproud.django.commons.views.decorators import render_to, ajax_request
from beproud.django.commons.views import Views


class TestViews(Views):
    def test(self, request):
        return HttpResponse("OK")

    def get_urls(self):
        urls = super(TestViews, self).get_urls()
        my_urls = [
            url(
                r'^test$',
                self.test,
                name='testview_test',
            ),
        ]
        return my_urls + urls


@render_to("view_tests/render_to.html")
def myview(request):
    return {"my_value": "MY VALUE"}


@render_to("view_tests/render_to.html")
def myview2(request):
    return HttpResponse("Error!")


@ajax_request
def my_ajax_view(request):
    return {'my_value': 'MY VALUE'}


@ajax_request
def my_ajax_view2(request):
    return HttpResponse("Error!")
