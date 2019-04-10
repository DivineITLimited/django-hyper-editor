import json

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.module_loading import import_string
from django.views.generic import TemplateView

from hypereditor import settings
from hypereditor.blocks import js_variable_str, get_js_plugins, get_simpler_blocks


class AuthMixin(UserPassesTestMixin, LoginRequiredMixin):
    """Helper mixin for authentication on hyper editor urls"""

    def test_func(self):
        return self.request.user.is_superuser


AuthenticationMixin = import_string(settings.AUTHENTICATION_MIXIN)


class EditorView(AuthenticationMixin, TemplateView):
    """View for hyper editor inside iframe"""

    template_name = 'hypereditor/hyper_editor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['block_settings'] = json.dumps(settings.BLOCK_CONFIG)
        context['user_stylesheets'] = settings.STYLESHEETS
        context['js_variables'] = js_variable_str
        context['js_plugins'] = get_js_plugins()
        context['image_api_url'] = settings.IMAGE_API_URL
        return context


class PreviewView(AuthenticationMixin, TemplateView):
    """View for preview of a single block"""

    http_method_names = ['post']
    template_name = 'hypereditor/preview.html'

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = json.loads(request.body)
        return self.render_to_response(context=context)


class GenerateBlock(AuthenticationMixin, TemplateView):
    template_name = 'hypereditor/js/blocks.js'

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response['Content-Type'] = 'application/javascript'
        return response

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={
            'blocks': get_simpler_blocks()
        })
