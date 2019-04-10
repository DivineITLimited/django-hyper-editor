from django.conf import settings
from django.apps import apps
from hypereditor import utils

WAGTAIL_EXISTS = apps.is_installed('wagtail.core')

HYPER_SETTINGS = {
    'BLOCK_CONFIG': {},
    'STYLESHEETS': [],
    'IMAGE_API_URL': '#',
    'AUTHENTICATION_MIXIN': 'hypereditor.views.AuthMixin'
}

utils.merge_dict(HYPER_SETTINGS, getattr(settings, 'HYPER_EDITOR', {}))

# A mixin class that will be used auth and permission of HyperEditor views
AUTHENTICATION_MIXIN = HYPER_SETTINGS['AUTHENTICATION_MIXIN']

# Provide styles or other things to block via settings
BLOCK_CONFIG = HYPER_SETTINGS['BLOCK_CONFIG']

# user defined stylesheet to look pretty
STYLESHEETS = HYPER_SETTINGS['STYLESHEETS']

# url that will be used as image api
IMAGE_API_URL = HYPER_SETTINGS['IMAGE_API_URL']
