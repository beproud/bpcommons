:mod:`commons.forms.fields` -- フォームフィールド
================================================================

.. module:: commons.forms.fields
   :synopsis:  フォームフィールド
.. moduleauthor:: Ian Lewis <ian@beproud.jp>


.. class:: commons.forms.fields.StripRegexField

    検証する前に、strip()をかけるフィールド。さらに、正規表現を指定した
    正規表現にマッチするかを検証します::

        from django import forms

        class MyForm(forms.Form):
            name = StripRegexField('^Monty', label=u'名前', error_message=u'名前はMontyから始まらないといけません。')
