:mod:`commons.http` -- HTTP ユティリティ
================================================================

.. module:: commons.http
   :synopsis:  HTTP ユティリティ
.. moduleauthor:: Ian Lewis <ian@beproud.jp>
.. currentmodule:: commons.http

.. class:: JSONResponse

    JSONデータを返すHTTPレスポンスです。 直列化できる Python オブジェクトを渡せば、
    自動で ``commons.utils.javascript.DjangoJSONEncoder`` を使って、JSONに変換します::
    
        from commons.http import JSONResponse

        def myview(request):
            ...
            if success:
                return JSONResponse({
                    "msg": u"登録成功しました。",
                    "id": obj.id,
                })
            else:
                return JSONResponse({
                    "msg": u"登録失敗しました。",
                }, status=400)
