from .base import Block
from django.conf import settings

BLOCK_REGISTRY = {}
EXCLUDED_LIST = getattr(settings, 'HYPER_EDITOR_EXCLUDE_BLOCKS', [])


def register_block(block_type, block_class):
    """Register a block
    :param block_type: str
    :param block_class: Block
    :return: None
    """
    if issubclass(block_class, Block):
        if block_type not in EXCLUDED_LIST: # Check if not explicitly excluded
            BLOCK_REGISTRY[block_type] = block_class
    else:
        raise Exception('%s is not a valid block class' % block_class)


def get_block_class_for(block_type):
    """Get a block from registry by type
    :param block_type: str
    :return: Block
    """
    return BLOCK_REGISTRY.get(block_type, Block)


def get_js_variables():
    js_variables = {}
    for k, v in BLOCK_REGISTRY.items():
        if issubclass(v, Block):
            if callable(v.JS_VARIABLES):
                to_add = v.JS_VARIABLES()
            else:
                to_add = v.JS_VARIABLES
            js_variables.update(to_add)
    return js_variables


def get_js_plugins():
    js_plugins = []
    for k, v in BLOCK_REGISTRY.items():
        if issubclass(v, Block):
            if v.JS_PLUGINS is not None:
                if isinstance(v.JS_PLUGINS, list):
                    js_plugins = js_plugins + v.JS_PLUGINS
                else:
                    js_plugins.append(v.JS_PLUGINS)
    return js_plugins


def register(block_type):
    """Convenient decorator for registering a block
    :param block_type: str
    """
    def wrap(cls):
        register_block(block_type, cls)
    return wrap
