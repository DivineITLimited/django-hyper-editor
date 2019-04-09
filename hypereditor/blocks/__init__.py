from .base import Block
import json
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


def js_variable_str():
    js_variables = {}
    for k, v in BLOCK_REGISTRY.items():
        if issubclass(v, Block):
            if callable(v.js_variables):
                to_add = v.js_variables()
            else:
                to_add = v.js_variables
            js_variables.update(to_add)
    return '\n'.join(['%s = `%s`;' % (k, v) for k, v in js_variables.items()])


def get_js_plugins():
    js_plugins = []
    for k, v in BLOCK_REGISTRY.items():
        if issubclass(v, Block):
            if v.js_files is not None:
                if isinstance(v.js_files, list):
                    js_plugins = js_plugins + v.js_files
                else:
                    js_plugins.append(v.js_files)
    return js_plugins


def get_simpler_blocks():
    result = {}
    for k, v in BLOCK_REGISTRY.items():
        config = v().get_block_config()
        if config:
            result[k] = json.dumps(config)
    return result


def register(block_type):
    """Convenient decorator for registering a block
    :param block_type: str
    """
    def wrap(cls):
        register_block(block_type, cls)
    return wrap
