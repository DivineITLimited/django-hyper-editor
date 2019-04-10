# Introduction

Django Hyper Editor is the official Django Integration of [Hyper Editor](https://github.com/DivineITLimited/hyper-editor).

Django Hyper Editor aims to provide an easy to use api for Hyper Editor blocks to cover most use cases.

# Installation

- Install Hyper Editor from pypi
```sybase
pip install hypereditor
```
- Add Hyper Editor to your ``INSTALLED_APPS``
```python
INSTALLED_APPS = [
    ...

    'hypereditor',

]
```
- Add Hyper Editor to your ``urls.py``
```python
urlpatterns = [
    path('hypereditor/', include('hypereditor.urls')),
    
    # if you are using Wagtail, then please add hypereditor urls before wagtail
]
```

Hyper Editor is installed in your project.