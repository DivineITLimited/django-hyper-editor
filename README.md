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

Current version 0.1.0-rc.1