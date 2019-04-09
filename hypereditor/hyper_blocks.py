from hypereditor.blocks.base import Block
from hypereditor.blocks import get_block_class_for, register


@register('column')
class ColumnBlock(Block):

    external = True

    def _build_col_class(self, colSettings):
        col_class = []
        if colSettings:
            for sz in ['XS', 'SM', 'MD', 'LG']:
                col_sz = colSettings.get('size' + sz, '12')
                tmp_sz = ['col']
                if sz != 'XS':
                    tmp_sz.append(sz.lower())
                tmp_sz.append(str(col_sz))
                col_class.append('-'.join(tmp_sz))

                tmp_off = ['offset']
                col_off = colSettings.get('offset' + sz)
                if col_off and col_off != '':
                    if sz != 'XS':
                        tmp_off.append(sz.lower())
                    tmp_off.append(str(col_off))
                    col_class.append('-'.join(tmp_off))
        return ' '.join(col_class)

    def get_context(self, value, parent_context=None):
        value['colClass'] = self._build_col_class(value.get('settings'))
        context = super().get_context(value, parent_context=parent_context)
        return context


@register('tab')
class TabBlock(Block):

    external = True

    def get_rendered_children(self, obj, context):
        if obj.get('children') is not None:

            total_childes = []
            for child in obj.get('children'):
                bl_class = get_block_class_for(child.get('type', 'INVALID_PLUGIN_WITH_NO_TYPE'))
                if bl_class:
                    instance = bl_class(self.codeRenderer)
                    rendered_child = instance.render(child, context)
                    total_childes.append({
                        'child': child,
                        'rendered': rendered_child
                    })
            return total_childes
        return []


@register('heading')
class Heading(Block):

    title = 'Heading'
    description = 'Heading Block'

    schema = {
        "fields": [
            {
                "type": "input",
                "inputType": "text",
                "label": "Heading Text",
                "model": "text"
            },
            {
                "type": "select",
                "label": "Heading Type",
                "model": "type",
                "values": [
                    "H1", "H2", "H3", "H4", "H5", "H6"
                ]
            }
        ]
    }

    initial = {
        "type": 'H3'
    }