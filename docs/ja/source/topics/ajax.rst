Ajax/JSONの処理
================================================================

ブラウザのJavascriptから、AJAXデータ通信をよくしますが、
面倒な部分はいっぱいあります。標準Djangoでは、HttpResponseで
mimetypeを指定した上、返すデータをJSONに直列化することも必要です。

.. code-block:: guess

    from django.contrib.auth.models import User
    from django.utils import simplejson

    def myajax_view(request):
        user = User.object.get(pk=request.GET["id"])
        return HttpResponse(simplejson.dumps({
            "username": user.username,
            "fullname": user.get_full_name(),
        }, mimetype="text/javascript")

上のやり方にしても、decimal.Decimal, datetime.datetime, DjangoのLazyObjectなどを
直列化することができません。

bpcommonsはAJAXをもっと簡単にできるようにいろなツールが揃えています。

``commons.views.decorators`` は ``ajax_view`` デコレーターを定義しています。

.. function:: ajax_request

    ajax_request をビュー関数につけると、ビューから返したデータをそのまま、
    JSONに書き換える::

        from django.contrib.auth.models import User
        from commons.views.decorators import ajax_request

        @ajax_request
        def myajax_view(request):
            user = User.object.get(pk=request.GET["id"])
            return {
                "username": user.username,
                "fullname": user.get_full_name(),
            }

    HttpResponse オブジェクトを返すこともできます。 HttpResponseを返した場合、
    response をajax_requestはJSONに変換せずにそのまま返す::

        from django.contrib.auth.models import User
        from commons.views.decorators import ajax_request

        @ajax_request
        def myajax_view(request):
            user = User.object.get(pk=request.GET["id"])
            if user != request.user:
                return HttpResponseBadRequest(u"不正なリクエスト")
            return {
                "username": user.username,
                "fullname": user.get_full_name(),
            }

