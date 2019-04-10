# Django Hyper Editor

Django integration for [Hyper Editor](https://github.com/divineitlimited/hyper-editor).

[![Documentation Status](https://readthedocs.org/projects/django-hyper-editor/badge/?version=latest)](https://django-hyper-editor.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

Install via pip

```sybase
pip install hypereditor
```

Add to ``settings.py``
```python
INSTALLED_APPS = [
    ...
    'hypereditor'
]
```

Add to ``urls.py``
```python
urlpatterns = [
    ...
    path('hypereditor/', include('hypereditor.urls')),
]
```

## Documentation

Please check the documentation site - [https://django-hyper-editor.readthedocs.io/en/latest/](https://django-hyper-editor.readthedocs.io/en/latest/)

## TODO
- [x] Hyper Editor Output Parser
- [x] Block System
- [x] Create simple block without using js
- [x] Django Model Integration ``HyperField``
- [x] Django Admin Integration
- [x] Django Form Integration
- [x] Wagtail Integration ``HyperFieldPanel``
- [x] Template tag for preview and render
- [x] Documentation
- [ ] Media Handling

## License
MIT

<sub>Made with :heart: at [Divine IT Limited](https://divineit.net/), Dhaka, Bangladesh</sup>