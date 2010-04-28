:mod:`commons.forms.fields` -- フォームフィールド
================================================================

.. module:: commons.forms.fields
   :synopsis:  フォームフィールド
.. moduleauthor:: Ian Lewis <ian@beproud.jp>
.. currentmodule:: commons.forms.fields

.. class:: StripRegexField

    検証する前に、strip()をかけるフィールド。さらに、正規表現を指定した
    正規表現にマッチするかを検証します::

        from django import forms
        from commons.forms import StripRegexField

        class MyForm(forms.Form):
            name = StripRegexField('^Monty', label=u'名前', error_message=u'名前はMontyから始まらないといけません。')

.. class:: EmailField

    Djangoは標準に電子メールアドレスのフォームフィールドクラスを用意してありますが、
    メールアドレスのフォーマットに厳しい。特に、日本の携帯メールアドレスが標準 Django
    の EmailField の検証に通らない。というわけで、commons.forms.fields で 
    EmailField が実装されています。

    使い方は Django の EmailField と一緒です::

        from django import forms
        from commons.forms import EmailField 

        class MyForm(forms.Form):
            email = EmailField(label=u"メールアドレス")

.. class:: AlphaNumField

    半角英数字と"_","-"のみ許容するフィールド::

        from django import forms

        class MyForm(forms.Form):
            username = AlphaNumField(label=u'ユーザ名')
