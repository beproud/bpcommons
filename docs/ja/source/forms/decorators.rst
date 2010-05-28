:mod:`commons.forms.decorators` -- フォームデコレーター
================================================================

.. module:: commons.forms.decorators
   :synopsis:  フォームデコレーター
.. moduleauthor:: Ian Lewis <ian@beproud.jp>
.. currentmodule:: commons.forms.decorators


.. function:: autostrip

    検証する前に、CharFieldのデータをstripするクラスデコレーター::

        class PersonForm(forms.Form):
            name = forms.CharField(min_length=2, max_length=10)
            email = forms.EmailField()

        PersonForm = autostrip(PersonForm)
 

