# vim:fileencoding=utf8
from django import template

__all__ = (
    'data_template_tag',
    'DataNode',
)

def data_template_tag(data_func, *args, **kwargs):
    """
    データを取ってくるタグ。

    data_funcはquerysetを返す関数

    使い方:
    @register.tag
    @data_template_tag
    def get_my_data():
        return MyData.objects.filter(...)

    テンプレートのほうは
    {% get_my_data as my_data %}
    
    引数も対応しています。

    @register.tag
    @data_template_tag
    def get_my_data(user):
        return MyData.objects.filter(user=user)

    {% get_my_data user as my_data %}

    キーワード引数も使えます
    """
    def wrapped(parser, token):
        bits = list(token.split_contents())

        args = []
        kwargs = {}
        name = None
        next_as = False 
        for bit in bits[1:]:
            if bit == 'as':
                next_as = True
            elif next_as:
                name = bit
                break
            else:
                if '=' in bit:
                    key, value = bit.split('=', 1)
                    if key and value:
                        kwargs[key] = value
                    else:
                        raise template.TemplateSyntaxError("invalid keyword arguments: %r" % bit)
                else:
                    args.append(bit)
                 
        if not name:
            raise template.TemplateSyntaxError("%r expected format is '%s *args **kwargs as <name>'" %
                                      (bits[0], bits[0]))
        return DataNode(data_func, args, kwargs, name)

    #名前を直す
    wrapped.__module__ = data_func.__module__
    wrapped.__name__ = data_func.__name__
    wrapped.__doc__ = data_func.__doc__
    return wrapped

class DataNode(template.Node):
    def __init__(self, data_func, args, kwargs, var_name):
        self.data_func = data_func 
        self.args = args
        self.kwargs = kwargs
        self.var_name = var_name

    def __repr__(self):
        return '<DataNode>'

    def render(self, context):
        args = [template.Variable(arg).resolve(context) for arg in self.args]
        kwargs = dict((str(key), template.Variable(value).resolve(context)) for key, value in self.kwargs.iteritems())
        context[self.var_name] = self.data_func(*args, **kwargs)
        return u''
