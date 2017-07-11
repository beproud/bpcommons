# vim:fileencoding=utf-8

from django.template import Node, Library, TemplateDoesNotExist, TemplateSyntaxError, Variable
from django.template.loader import render_to_string

register = Library()

class GoogleAdNode(Node):
    def __init__(self, template_name_var, block_id_var=None):
        self.block_id_var = Variable(block_id_var) if block_id_var else None
        self.template_name_var = Variable(template_name_var)

    def render(self, context):
        try:
            block_id = self.block_id_var.resolve(context) if self.block_id_var else None;
            template_name = self.template_name_var.resolve(context)
            context_dict = {
                "block_id": block_id if block_id else "",
            }
            for c in context.dicts:
                context_dict.update(c)

            return render_to_string(template_name, context_dict)

        except TemplateDoesNotExist as e:
            return ''

@register.tag
def googlead(parser, token):
    bits = token.split_contents()
    if len(bits) != 2 and len(bits) != 3:
        raise TemplateSyntaxError("%r takes at least one argument." % bits[0])
    template_name = bits[1]
    if len(bits) == 3:
        return GoogleAdNode(template_name, bits[2])
    else:
        return GoogleAdNode(template_name)
