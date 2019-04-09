{% for block_type, config in blocks.items %}
    hyperEditor.registerBlock('{{ block_type }}', JSON.parse('{{ config|safe }}'))
{% endfor %}