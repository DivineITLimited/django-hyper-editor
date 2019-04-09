import json

from django.conf import settings
from django.http.response import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView

from hypereditor.blocks import js_variable_str, get_js_plugins, get_simpler_blocks


class AuthenticationMixin(UserPassesTestMixin, LoginRequiredMixin):
    """Helper mixin for authentication on hyper editor urls"""

    def test_func(self):
        return self.request.user.is_superuser


class EditorView(AuthenticationMixin, TemplateView):
    """View for hyper editor inside iframe"""

    template_name = 'hypereditor/hyper_editor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        block_settings = getattr(settings, 'HYPER_EDITOR_BLOCK_CONFIG', {})
        user_stylesheets = getattr(settings, 'HYPER_EDITOR_USER_STYLESHEETS', [])
        context['block_settings'] = json.dumps(block_settings)
        context['user_stylesheets'] = user_stylesheets
        context['js_variables'] = js_variable_str
        context['js_plugins'] = get_js_plugins()
        context['image_api_url'] = getattr(settings, 'HYPER_IMAGE_API', '#')
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