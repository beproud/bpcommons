:mod:`commons.middleware.debug` -- デバグ ミドルウエア
================================================================

.. module:: commons.middleware.debug
   :synopsis:  デバグ ミドルウエア
.. moduleauthor:: Shinya Okano <shinya.okano@beproud.jp>
.. currentmodule:: commons.middleware.debug

.. class:: DebugMiddleware 

    SQLクエリをstdoutに出力するミドルウエア。``settings.DEBUG`` は True である場合のみに、
    クエリを出力します。
