import json
from django.test import SimpleTestCase
from django.template import Context, Template
from hypereditor.tests import mocks


class HyperRenderTemplateTagTest(SimpleTestCase):
    """Tests for hyper_render template tag"""

    def test_render(self):
        context = Context({'content': json.dumps([mocks.TEXT_BLOCK])})
        template_to_render = Template(
            '{% load hyper_tags %}'
            '{% hyper_render content %}'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<div id="i1554530213_4">\nSample Text\n</div>', rendered_template)


class HyperPreviewTemplateTagTest(SimpleTestCase):
    """Tests for hyper_preview template tag"""

    def test_preview(self):
        context = Context({'content': mocks.TEXT_BLOCK})
        template_to_render = Template(
            '{% load hyper_tags %}'
            '{% hyper_preview content %}'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<div id="i1554530213_4">\nSample Text\n</div>', rendered_template)

