from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import Template, Context, RequestContext
from hypereditor.utils import dict_to_css


class CodeRenderer(object):
    """An Utility Class for Generating CSS and JS"""

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


class Block(object):
    """Base Block Class"""

    TEMPLATE_VAR = 'obj'
    JS_VARIABLES = {}
    JS_PLUGINS = None

    def __init__(self, codeRenderer):
        if isinstance(codeRenderer, CodeRenderer):
            self.codeRenderer = codeRenderer
        else:
            raise Exception('Invalid Renderer')

    def get_template(self, obj):
        style = obj.get('general', {}).get('style', 'default')
        return 'hypereditor/blocks/{type}/{style}.html'.format(type=obj['type'], style=style)

    def get_context(self, value, parent_context=None):
        context = parent_context or {}
        context.update({
            'self': value,
            self.TEMPLATE_VAR: value,
        })
        return context

    def get_rendered_children(self, obj, context=None):
        rendered_child = ''
        if obj.get('children') is not None:
            from . import get_block_class_for
            for child in obj.get('children'):
                bl_class = get_block_class_for(child.get('type', 'INVALID_PLUGIN_WITH_NO_TYPE'))
                if bl_class:
                    instance = bl_class(self.codeRenderer)
                    rendered_child = rendered_child + instance.render(child, context)
        return mark_safe(rendered_child)

    def _prepare_custom_codes(self, obj):
        if obj.get('extra'):
            if obj['extra'].get('cssCode'):
                self.codeRenderer.add_css(obj['extra']['cssCode'])
            if obj['extra'].get('jsCode'):
                self.codeRenderer.add_css(obj['extra']['jsCode'])

    def render(self, obj, context=None):
        if isinstance(context, Context) or isinstance(context, RequestContext):
            context = context.flatten()
        self._prepare_custom_codes(obj)
        self.generate_inline_css(obj)

        rendered_child = self.get_rendered_children(obj, context)

        if context is None:
            new_context = self.get_context(obj)
        else:
            new_context = self.get_context(obj, parent_context=context)

        new_context['children'] = rendered_child

        if obj.get('extra', {}).get('htmlCode'):
            html_code = obj['extra'].get('htmlCode').strip()
            if len(html_code) > 0:
                template = Template(html_code)
                c = Context(new_context)
                return mark_safe(template.render(c))

        template = self.get_template(obj)

        return mark_safe(render_to_string(template, new_context))

    def generate_inline_css(self, obj):
        inline_css = {}
        if obj.get('general'):
            general = obj['general']
            if general.get('padding'):
                inline_css.update(self._build_padding(general['padding']))
            if general.get('margin'):
                inline_css.update(self._build_padding(general['margin']))
            if general.get('backgroundImage'):
                inline_css.update(self._build_background_image(general['backgroundImage']))
            if general.get('backgroundColor'):
                inline_css.update(self._build_background_color(general['backgroundColor']))
            if general.get('foregroundColor'):
                inline_css.update(self._build_foreground_color(general['foregroundColor']))
            if general.get('textAlignment'):
                inline_css.update({ 'text-align': general['textAlignment']})
        if len(inline_css) > 0:
            self.codeRenderer.addCSS(dict_to_css({'#'+obj['id']: inline_css}))

    def _build_background_image(self, image):
        return {
            'background': 'url("' + image['url'] + '")',
            'background-repeat': 'no-repeat',
            'background-size': 'cover'
        }

    def _build_background_color(self, bgcolor):
        return {
            'background-color': 'rgba({r}, {g}, {b}, {a})'.format(
                r=bgcolor.get('r'),
                g=bgcolor.get('g'),
                b=bgcolor.get('b'),
                a=bgcolor.get('a')
            )
        }

    def _build_foreground_color(self, fgcolor):
        return {
            'color': 'rgba({r}, {g}, {b}, {a})'.format(
                r=fgcolor.get('r'),
                g=fgcolor.get('g'),
                b=fgcolor.get('b'),
                a=fgcolor.get('a')
            )
        }

    def _build_padding(self, padding):
        padding_dict = {}
        for key, val in padding.items():
            if key != 'unit' and val is not None:
                padding_dict['padding-'+key] = val + padding['unit']
        return padding_dict

    def _build_margin(self, margin):
        margin_dict = {}
        for key, val in margin.items():
            if key != 'unit' and val is not None:
                margin_dict['margin-'+key] = val + margin['unit']
        return margin_dict


