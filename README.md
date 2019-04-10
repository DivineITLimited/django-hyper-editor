# Django Hyper Editor

Django integration for [Hyper Editor](https://github.com/divineitlimited/hyper-editor).


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

Current version 0.1.0-rc.3

## TODO
- [x] Hyper Editor Output Parser
- [x] Block System
- [x] Create simple block without using js
- [x] Django Model Integration ``HyperField``
- [x] Django Admin Integration
- [x] Django Form Integration
- [x] Wagtail Integration ``HyperFieldPanel``
- [x] Template tag for preview and render
- [ ] Media Handling
- [ ] Documentation