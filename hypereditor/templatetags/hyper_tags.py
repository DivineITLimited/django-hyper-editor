from django import template
from hypereditor.blocks import get_block_class_for
from hypereditor.blocks.base import CodeRenderer
from hypereditor.fields import HyperFieldResponse
from django.template.defaulttags import token_kwargs
register = template.Library()


class HyperNode(template.Node):

    def __init__(self, block_var, extra_context, use_parent_context):
        self.block_var = block_var
        self.extra_context = extra_context
        self.use_parent_context = use_parent_context

    def render(self, context):
        try:
            value = self.block_var.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        if isinstance(value, dict): # its an preview
            code_renderer = CodeRenderer()
            bl_class = get_block_class_for(value.get('type', 'INVALID_PLUGIN_WITH_NO_TYPE'))
            if bl_class:
                instance = bl_class(value, code_renderer)
                return instance.render(context)
            else:
                return ''
        elif isinstance(value, str):
            try:
                value = HyperFieldResponse.from_str(value)
                return value.render(context)
            except Exception as e:
                print(e)
                return ''
        else:
            return value.render(context)


def __render_helper(parser, token):

    tokens = token.split_contents()

    try:
        tag_name = tokens.pop(0)
        block_var_token = tokens.pop(0)
    except IndexError:
        raise template.TemplateSyntaxError("%r tag requires at least one argument" % tag_name)

    block_var = parser.compile_filter(block_var_token)

    if tokens and tokens[0] == 'with':
        tokens.pop(0)
        extra_context = token_kwargs(tokens, parser)
    else:
        extra_context = None

    use_parent_context = True
    if tokens and tokens[0] == 'only':
        tokens.pop(0)
        use_parent_context = False

    if tokens:
        raise template.TemplateSyntaxError("Unexpected argument to %r tag: %r" % (tag_name, tokens[0]))

    return HyperNode(block_var, extra_context, use_parent_context)


@register.tag
def hyper_render(parser, token):
    return __render_helper(parser, token)


@register.tag
def hyper_preview(parser, token):
    return __render_helper(parser, token)

