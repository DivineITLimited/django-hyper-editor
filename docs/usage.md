# Usage

Using Hyper Editor is pretty easy. Checkout appropriate section that you are interested in.

## Django Model

You can easily use Hyper Editor as a Model field like following -

```python
from django.db import models

# import Hyper Editor Field
from hypereditor.fields import HyperField


class Page(models.Model):
    title = models.CharField(max_length=255)
    
    # Use just like any other field
    content = HyperField(default=None)
    
    def __str__(self):
        return self.title
```

## Django Forms

Model Forms will work out of the box. For example for the previous model ``Page``

```python
from django import forms


class PageForm(forms.ModelForm):

    class Meta:
        model = models.Page
        exclude = []
```

For Regular Form you can use it like following -

```python
from django import forms
from hypereditor.fields import HyperFormField


class TestForm(forms.Form):
    
    content = HyperFormField()

```

## Django Admin

Works out of the box just like ``ModelForm``. Just register your model.

```python
from django.contrib import admin
from sandbox.example.models import *


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
```

## Rendering

You need to use ``hyper_tags`` in your template in order to display Hyper Editor Generated Contents.

```html
{% load hyper_tags %}

{% hyper_render page.content %}
```
