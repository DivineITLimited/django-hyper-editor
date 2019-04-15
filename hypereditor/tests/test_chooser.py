from django.test import TransactionTestCase
from sandbox.example.models import Page
from hypereditor.blocks.chooser import Chooser


class PageChooser(Chooser):
    queryset = Page.objects.filter()


class PageChooser2(Chooser):
    queryset = Page.objects.filter()
    fields = ['title', 'id']


class ChooserTestCase(TransactionTestCase):

    def setUp(self):
        for count in range(0, 40):
            Page.objects.create(title='Test %s' % count, content='[]')

    def test_chooser(self):
        page_chooser = PageChooser()
        result = page_chooser.paginate(None, None)
        self.assertEqual(result['total'], 40)

    def test_chooser2(self):
        page_chooser = PageChooser2()
        result = page_chooser.paginate(None, None)
        self.assertEqual(result['total'], 40)
