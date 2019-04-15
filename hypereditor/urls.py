from django.conf.urls import include, url
from hypereditor.views import *

app_name = 'hypereditor'

urlpatterns = [
    url(r'editor/$', EditorView.as_view(), name='editor'),
    url(r'preview/', PreviewView.as_view(), name='preview'),
    url(r'chooser-api/(?P<chooser_type>\w{0,50})/', ChooserAPIView.as_view(), name='chooser_api'),
    url(r'js/blocks', GenerateBlock.as_view(), name='blocks')
]
