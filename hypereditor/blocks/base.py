from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import Template, Context, RequestContext
from hypereditor.utils import dict_to_css


class CodeRenderer(object):
    """An Utility Class for Collecting CSS and JS from all Blocks in Node Tree"""

    css = []
    js = []

    def add_css(self, css):
        if css:
            css = css.strip()
            if len(css) > 0:
                self.css.append(css)

    def add_js(self, js):
        if js:
            js = js.strip()
            if len(js) > 0:
                self.js.append(js)

    def render_css(self):
        return '<style type="text/css">' + '\n'.join(self.css) + '</style>'

    def render_js(self):
        return '<script type="text/javascript">'+'\n'.join(self.js)+'</script>'


def _build_background_image(image):
    return {
        'background': 'url("' + image['url'] + '")',
        'background-repeat': 'no-repeat',
        'background-size': 'cover'
    }


def _build_background_color(bgcolor):
    return {
        'background-color': 'rgba({r}, {g}, {b}, {a})'.format(
            r=bgcolor.get('r'),
            g=bgcolor.get('g'),
            b=bgcolor.get('b'),
            a=bgcolor.get('a')
        )
    }


def _build_foreground_color(fgcolor):
    return {
        'color': 'rgba({r}, {g}, {b}, {a})'.format(
            r=fgcolor.get('r'),
            g=fgcolor.get('g'),
            b=fgcolor.get('b'),
            a=fgcolor.get('a')
        )
    }


def _build_padding(padding):
    padding_dict = {}
    for key, val in padding.items():
        if key != 'unit' and val is not None:
            padding_dict['padding-'+key] = val + padding['unit']
    return padding_dict


def _build_margin(margin):
    margin_dict = {}
    for key, val in margin.items():
        if key != 'unit' and val is not None:
            margin_dict['margin-'+key] = val + margin['unit']
    return margin_dict


class Block(object):
    """Base Block Class"""

    # template variable to be used
    template_var = 'obj'

    # if any js variables required to initialize
    js_variables = {}

    # if any js file needs to be initialized
    js_files = None

    # for simple block following variables can be used
    external = False
    title = None
    description = None
    schema = None
    initial = None
    general_initial = None
    styles = None

    def __init__(self, obj={}, code_renderer=None):
        """
        Initialize block
        :param obj: dict - The value object for this block in tree
        :param code_renderer: instance of CodeRenderer
        """
        self.obj = obj
        if code_renderer and isinstance(code_renderer, CodeRenderer):
            self.codeRenderer = code_renderer
        elif code_renderer:
            raise Exception('Invalid Renderer')

    def get_template(self):
        """
        Determine which template to use. A block might have multiple style.
        Each style has its own template.
        :return: str - template name
        """
        style = self.obj.get('general', {}).get('style', 'default')
        return 'hypereditor/blocks/{type}/{style}.html'.format(type=self.obj['type'], style=style)

    def get_context(self, parent_context=None):
        """
        Build Block Context. Assign parent context if has any.
        :param parent_context: dict
        :return: dict
        """
        context = parent_context or {}
        context.update({
            'self': self.obj,
            self.template_var: self.obj,
        })
        return context

    def get_rendered_children(self, context=None):
        """
        Blocks might have child blocks. Render children.
        :param context: dict context for children
        :return: safe str - Rendered string
        """
        from hypereditor.blocks import get_block_class_for
        rendered_child = ''
        if self.obj.get('children') is not None:
            for child in self.obj.get('children'):
                bl_class = get_block_class_for(child.get('type', 'INVALID_PLUGIN_WITH_NO_TYPE'))
                if bl_class:
                    instance = bl_class(child, self.codeRenderer)
                    rendered_child = rendered_child + instance.render(context)
        return mark_safe(rendered_child)

    def _prepare_custom_codes(self):
        """
        If any extra css or js added from editor add them to code_renderer
        :return: None
        """
        if self.obj.get('extra'):
            if self.obj['extra'].get('cssCode'):
                self.codeRenderer.add_css(self.obj['extra']['cssCode'])
            if self.obj['extra'].get('jsCode'):
                self.codeRenderer.add_css(self.obj['extra']['jsCode'])

    def render(self, context=None):
        """
        Render Block
        :param context: dict - block context
        :return: safe str: Rendered str
        """
        if isinstance(context, Context) or isinstance(context, RequestContext):
            context = context.flatten()
        self._prepare_custom_codes()
        self.build_general_settings()

        rendered_child = self.get_rendered_children(context)

        if context is None:
            new_context = self.get_context()
        else:
            new_context = self.get_context(parent_context=context)

        new_context['children'] = rendered_child

        if self.obj.get('extra', {}).get('htmlCode'):
            html_code = self.obj['extra'].get('htmlCode').strip()
            if len(html_code) > 0:
                template = Template(html_code)
                c = Context(new_context)
                return mark_safe(template.render(c))

        template = self.get_template()

        return mark_safe(render_to_string(template, new_context))

    def build_general_settings(self):
        """
        General settings contains CSS properties. Add them to code_renderer
        :return: None
        """
        inline_css = {}
        if self.obj.get('general'):
            general = self.obj['general']
            if general.get('padding'):
                inline_css.update(_build_padding(general['padding']))
            if general.get('margin'):
                inline_css.update(_build_padding(general['margin']))
            if general.get('backgroundImage'):
                inline_css.update(_build_background_image(general['backgroundImage']))
            if general.get('backgroundColor'):
                inline_css.update(_build_background_color(general['backgroundColor']))
            if general.get('foregroundColor'):
                inline_css.update(_build_foreground_color(general['foregroundColor']))
            if general.get('textAlignment'):
                inline_css.update({'text-align': general['textAlignment']})
        if len(inline_css) > 0:
            self.codeRenderer.add_css(dict_to_css({'#%s' % self.obj['id']: inline_css}))

    def get_block_config(self):
        """
        Build minimal block using python
        :return: dict / None - containing block info or None
        """
        if not self.external:
            default_values = {
                'settings': self.initial if self.initial else {},
                'general': self.general_initial if self.general_initial else {}
            }

            result = {
                "title": self.title,
                "description": self.description,
                "settings_schema": self.schema,
                "default_values": default_values,
                "config": {
                    "styles": self.styles if self.styles else [{"id": 'default', "name": 'Default'}]
                }

            }
            return result
        else:
            return None
