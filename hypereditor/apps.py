from django.apps import AppConfig
from hypereditor.utils import load_hyper_blocks


class HyperEditorConfig(AppConfig):
    name = 'hypereditor'

    def ready(self):
        super().ready()
        # load all hyper_blocks.py
        list(load_hyper_blocks())
