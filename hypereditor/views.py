import json

from django.conf import settings
from django.views.generic import TemplateView
from hypereditor.blocks import get_js_variables, get_js_plugins


class EditorView(TemplateView):

    template_name = 'hypereditor/hyper_editor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        block_settings = getattr(settings, 'HYPER_EDITOR_BLOCK_CONFIG', {})
        user_stylesheets = getattr(settings, 'HYPER_EDITOR_USER_STYLESHEETS', [])
        context['block_settings'] = json.dumps(block_settings)
        context['user_stylesheets'] = user_stylesheets
        context['js_variables'] = get_js_variables()
        context['js_plugins'] = get_js_plugins()
        context['image_api_url'] = getattr(settings, 'HYPER_IMAGE_API', '#')
        return context


class PreviewView(TemplateView):
    http_method_names = ['post']
    template_name = 'hypereditor/preview.html'

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = json.loads(request.body)
        return self.render_to_response(context=context)
