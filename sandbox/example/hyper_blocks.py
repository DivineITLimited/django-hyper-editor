from sandbox.example.models import Page
from hypereditor.blocks import Chooser, register_chooser


@register_chooser('page_chooser')
class PageChooser(Chooser):
    queryset = Page.objects.filter()
    fields = ['id', 'title']
    search_fields = ['title']