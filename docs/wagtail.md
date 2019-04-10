# Wagtail

Django Hyper Editor has good support for wagtail too. 

While using with Wagtail use ``HyperFieldPanel`` instead of ``FieldPanel``

```python
from hypereditor.fields import HyperFieldPanel


content_panels = [
    # Other panels
    HyperFieldPanel('field_name')
]
```