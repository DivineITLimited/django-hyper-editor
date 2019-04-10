from importlib import import_module
import collections
from django.apps import apps
from django.utils.module_loading import module_has_submodule


def dict_to_css(css_dict, pretty=False):
    """Takes a dictionary and creates CSS from it
    :param css_dict: python dictionary containing css rules
    :param pretty: if css should be generated as pretty
    :return: css as string
    """
    seperator = '\n'
    tab = '\t'
    if not pretty:
        seperator = ''
        tab = ''

    css_rules = []
    for selector, rules in css_dict.items():
        tmp = selector + '{' + seperator
        tmp_rules = []
        if isinstance(rules, dict):
            for rule, value in rules.items():
                tmp_rules.append(tab + rule + ':' + value + ';')
        tmp += seperator.join(tmp_rules)
        tmp = tmp + '}'
        css_rules.append(tmp)

    return seperator.join(css_rules)


def dynamic_import(val):
    """Imports a python module dynamically
    :param val: String module path
    :return: None
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import '%s' for setting. %s: %s." % (val, e.__class__.__name__, e)
        raise ImportError(msg)


def get_app_modules():
    for app in apps.get_app_configs():
        yield app.name, app.module


def load_hyper_blocks():
    submodule_name = 'hyper_blocks'
    for name, module in get_app_modules():
        if module_has_submodule(module, submodule_name):
            yield name, import_module('%s.%s' % (name, submodule_name))


def merge_dict(d, m_d):
    """
    Given two dictionary, merge m_d dictionary into d
    :param d: dict
    :param m_d: dict
    :return: None
    """
    for k, v in m_d.items():
        if k in d and isinstance(d[k], dict) and isinstance(d[k], collections.Mapping):
            merge_dict(d[k], m_d[k])
        else:
            d[k] = m_d[k]
