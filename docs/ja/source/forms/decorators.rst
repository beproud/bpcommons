:mod:`commons.forms.decorators` -- フォームデコレーター
================================================================

.. module:: commons.forms.decorators
   :synopsis:  フォームデコレーター
.. moduleauthor:: Ian Lewis <ian@beproud.jp>


.. function:: commons.forms.decorators.autostrip

    検証する前に、CharFieldのデータをstripするクラスデコレーター::

        class PersonForm(forms.Form):
            name = forms.CharField(min_length=2, max_length=10)
            email = forms.EmailField()

        PersonForm = autostrip(PersonForm)
 

