:mod:`commons.forms.utils` -- フォームユティリティ
================================================================

.. module:: commons.forms.utils
   :synopsis:  データユティリティクラス
.. moduleauthor:: Ian Lewis <ian@beproud.jp>


.. class:: commons.forms.utils.Choices

    ChoicesはDjangoのforms.ChoiceFieldに使える便利なクラス。普段には
    ChoiceFieldのchoicesパラメータとして、2-tupleを使いますが、実は
    イテレータオブジェクトも使えます。Choicesは整数とverboseと文字列名前
    をマッピングしてくれて、便利な操作ができます。::

        >>> from commons.forms import Choices
        
        >>> STATUSES = Choices(
        ...     (1, 'live', 'Live'),
        ...     (2, 'draft', 'Draft'),
        ...     (3, 'hidden', 'Not Live'),
        ... )
        
        # choicesリストとして使えます:
        >>> list(STATUSES)
        [(1, 'Live'), (2, 'Draft')]
        
        # 整数コードから、ラベルに簡単に変換:
        >>> STATUSES.verbose(1)
        'Live'

        # 文字列名前にマッピング
        >>> STATUS.prop(1)
        'live'
        
        # ... と逆に:
        >>> STATUSES.code("draft")
        2

        # モデルフィールドにchoicesとして使えます
        status = models.SmallIntegerField(choices=STATUSES,
        ...                                       default=STATUSES["live"])
        
