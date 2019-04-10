# Blocks

[Hyper Editor](https://github.com/DivineITLimited/hyper-editor) is a block based content editor. 
You might want to create different kinds of block that then be used in the frontend editor.

There are two different way you can create block. In both cases you are going to extend 
``hypereditor.blocks.base.Block`` class.

## hyper_blocks.py

It might be better to separate Hyper Editor blocks from other codes of your project.
That is why we will use ``hyper_blocks.py`` file to keep our blocks.

Create a file named ``hyper_blocks.py`` in your django app where ``models.py``, ``views.py`` resides (in application folder).

## Simple Blocks

Lets create a simple heading block.

```python
from hypereditor.blocks.base import Block
from hypereditor.blocks import register


# register block with a block_type parameter
@register('heading')
class Heading(Block):
    
    # Title & Description of your block as seen at HyperEditor block chooser
    title = 'Heading'
    description = 'Heading Block'
    
    # Your settings fields for block
    schema = {
        "fields": [
            {
                "type": "input",
                "inputType": "text",
                "label": "Heading Text",
                "model": "text"
            },
            {
                "type": "select",
                "label": "Heading Type",
                "model": "type",
                "values": ['h{0}'.format(i) for i in range(1, 7)]
            }
        ]
    }
    
    # Initial values for your settings field
    initial = {
        "type": 'h3'
    }
```

You should see your Heading block is now showing in Hyper Editor.

## Block Templates

Each block must have at least one **template**. **Templates** are related to **Block Styles** in Hyper Editor.

Lets create a default template for our heading block.

- Create a directory called ``hypereditor`` in your ``templates`` folder.

- Create another directory called ``blocks`` inside ``hypereditor`` folder.

- Create another directory with the same name of your ``block_type``

- Create a template named ``default.html``

Your folder structure should look like following -
```sybase
├── templates
│   └── hypereditor
│       ├── blocks
│       │   ├── heading
│       │   │   └── default.html
```

It might look like a bit much, but we found it helps us separating when there are lots of blocks.

Now add following in your template -
```djangotemplate
<{{ obj.settings.type }}>
    {{ obj.settings.text }}
</{{ obj.settings.type }}>
```

### Template Context

Yet to be documented

## Advance Blocks

Yet to be documented.